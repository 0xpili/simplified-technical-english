#!/usr/bin/env python3
"""ste_check.py - a check tool for ASD-STE100 Simplified Technical English.

This tool finds violations of the STE writing rules in text or Markdown.
It uses only the Python standard library.

Usage:
    python3 ste_check.py [--mode procedural|descriptive|mixed] [--allow NAMES] FILE...
    cat draft.txt | python3 ste_check.py --mode procedural

The tool ignores code blocks, inline code, URLs, and YAML frontmatter.
Exit code 0 = no errors. Exit code 1 = one or more errors.
"""

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- constants

# Rule 3.5: the only approved "-ing" words in the STE dictionary.
ING_APPROVED = {
    "mating", "missing", "remaining",          # adjectives
    "lighting", "opening", "routing", "servicing",  # nouns
    "during",                                  # preposition
}

# Words that end in "ing" where "ing" is not a verb suffix.
ING_NOT_SUFFIX = {
    "ring", "spring", "string", "king", "thing", "wing", "sing",
    "bring", "sting", "swing", "nothing", "anything", "everything",
    "something", "bearing", "ceiling", "morning", "evening",
    # frequent nouns and technical names that are not verb forms
    "warning", "meaning", "spelling", "heading", "building", "housing",
    "fitting", "wiring", "coupling", "drawing", "bushing", "tubing",
    "lining", "casing", "padding", "spacing",
}

# Words that the vocabulary check accepts without the word list:
# the article "a", signal words of safety instructions (rule 7.1),
# and numbers (technical name category 9).
VOCAB_EXTRA = {
    "a", "warning", "caution", "note",
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "twenty", "thirty", "forty", "fifty",
    "hundred", "thousand", "first", "second", "third",
}

# Abbreviations that end with a full stop but do not end a sentence.
# The second group does not end a sentence only before a number.
ABBREV = re.compile(
    r"\b(?:e\.g|i\.e|cf|vs|approx)\.|"
    r"\b(?:Fig|Figs|No|Nos|Ref|Para|Vol|Rev|Sect|Chap|Tab)\.(?=\s+\d)",
    re.IGNORECASE,
)

# Rule 8.6: a number, or a number with its unit, counts as one word.
UNITS = (
    r"°\s?[CF]|%|N\.m|Nm|lbf\.in|lbf\.ft|lbf|psi|bar|kPa|MPa|Pa|"
    r"mm|cm|km|m|ft|mi|kg|mg|g|lb|oz|mL|ml|L|l|"
    r"kV|mV|V|mA|A|kW|mW|W|ohms?|Ω|kHz|MHz|GHz|Hz|"
    r"ms|s|min|h|rpm|K|dB|KB|MB|GB|TB|kB|B"
)
NUMBER_UNIT = re.compile(
    r"(?<![\w.])[-+]?\d+(?:[.,]\d+)*(?:\s?(?:" + UNITS + r"))?(?!\w)(?!\.\w)"
)

# Rule 3.2 and the dictionary: approved helping verbs are CAN, MUST, WILL.
BANNED_MODALS = {"should", "would", "may", "might", "shall", "ought"}

CONTRACTION = re.compile(
    r"\b\w+n['’]t\b|\b\w+['’](?:re|ll|ve|m|d)\b|"
    r"\b(?:it|that|there|what|let|who|here|he|she)['’]s\b",
    re.IGNORECASE,
)

HAVE_PARTICIPLE = re.compile(
    r"\b(?:has|have|had)\s+(?:been|\w+ed|done|made|gone|put|set|cut|kept|held|"
    r"taken|given|found|left|lost|meant|sent|shown|told|built|become|begun|"
    r"broken|brought|come|fallen|felt|got|gotten|grown|known|read|run|seen|"
    r"spoken|thrown|worn|written)\b",
    re.IGNORECASE,
)

COMPLEX_PASSIVE = re.compile(
    r"\b(?:can|will|must|could|would|should|may|might|shall)\s+"
    r"(?:not\s+)?be\s+\w+(?:ed|en)\b|"
    r"\b(?:is|are|was|were)\s+to\s+be\s+\w+(?:ed|en)\b",
    re.IGNORECASE,
)

PASSIVE_BY = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+\s+)?\w+(?:ed|en)\s+by\b",
    re.IGNORECASE,
)

BE_ING = re.compile(
    r"\b(?:is|are|was|were|be|been|am)\s+\w+ing\b", re.IGNORECASE
)

# A past participle after "was" or "were" is almost always a passive
# (rule 3.6). After "is" or "are" it can show a condition (rule 3.3).
PAST_PASSIVE = re.compile(
    r"\b(?:was|were)\s+(?:not\s+)?(?:\w+ed|done|made|put|set|cut|kept|held|"
    r"taken|given|found|left|lost|sent|shown|told|built|broken|brought|"
    r"known|read|run|seen|thrown|worn|written)\b",
    re.IGNORECASE,
)

SENT_SPLIT = re.compile(r"(?<=[.!?:])\s+")
ABBREV_MARK = "\x00"
WORDISH = re.compile(r"[A-Za-z0-9'&/’-]+")

LIMITS = {"procedural": 20, "descriptive": 25, "mixed": 25}


# ---------------------------------------------------------------- helpers

def strip_markdown(text):
    """Remove parts of the text that the STE rules do not control."""
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)   # frontmatter
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)          # code blocks
    text = drop_indented_code(text)                                  # code blocks
    text = re.sub(r"`[^`\n]+`", " CODE ", text)                      # inline code
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)             # links
    text = re.sub(r"https?://\S+", " URL ", text)                    # bare URLs
    text = re.sub(r"^>.*$", " ", text, flags=re.MULTILINE)           # block quotes
    # quoted text counts as one word and is not controlled (rule 8.6)
    text = re.sub(r"\"[^\"\n]*\"|“[^”\n]*”", " QUOTED ", text)
    return text


def drop_indented_code(text):
    """Remove indented code blocks (4 spaces or a tab on each line).

    A block that starts with a list marker is a nested list, not code.
    """
    parts = re.split(r"(\n[ \t]*\n)", text)
    for i, part in enumerate(parts):
        lines = [l for l in part.splitlines() if l.strip()]
        if (lines
                and all(re.match(r"(?: {4,}|\t)", l) for l in lines)
                and not re.match(r"\s*(?:[-*+]|\d+\.)\s", lines[0])):
            parts[i] = " "
    return "".join(parts)


def count_words(sentence):
    """Count words with the STE conventions of section 8.

    A number, a number with its unit, an abbreviation, an identifier,
    a hyphenated group, and text in parentheses each count as one word.
    """
    s = re.sub(r"\([^)]*\)", " PAREN ", sentence)   # rule 8.5
    s = ABBREV.sub(" ABBR ", s)                     # rule 8.6
    s = NUMBER_UNIT.sub(" NUM ", s)                 # rule 8.6
    s = re.sub(r"\*\*|\*|__|_|#+", " ", s)          # markdown marks
    tokens = WORDISH.findall(s)                     # hyphenated group = 1 (rule 8.7)
    return len(tokens)


def iter_sentences(block):
    """Divide a text block into sentences.

    A full stop in an abbreviation ("e.g.", "Fig. 2") does not end a sentence.
    """
    block = ABBREV.sub(lambda m: m.group(0).replace(".", ABBREV_MARK), block)
    for part in SENT_SPLIT.split(block):
        part = part.replace(ABBREV_MARK, ".").strip()
        if part and WORDISH.search(part):
            yield part


def load_word_list(path):
    """Read word-list.md and return the set of approved word forms."""
    approved = set()
    line_re = re.compile(r"^([A-Z][A-Z' -]*[A-Z])\s+\((\w+(?:, \w+)*)\)(?:\s+\[(.*)\])?")
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = line_re.match(line)
        if not m:
            continue
        head, _pos, forms = m.groups()
        for w in head.split():
            approved.add(w.lower())
        if forms:
            for f in forms.split(","):
                for w in f.strip().split():
                    approved.add(w.lower())
        # plurals of nouns (rule: plural of a countable noun is approved)
        if "(n)" in line:
            word = head.lower()
            approved.add(word + "s")
            if word.endswith(("s", "x", "ch", "sh")):
                approved.add(word + "es")
            if word.endswith("y") and word[-2:-1] not in "aeiou":
                approved.add(word[:-1] + "ies")
    return approved


def load_allow_list(path):
    """Read a file of technical names. Lines that start with "#" are comments."""
    allowed = set()
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        for w in re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", line):
            allowed.add(w.lower())
    return allowed


# ---------------------------------------------------------------- checks

class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.unknown = {}

    def error(self, loc, rule, msg):
        self.errors.append((loc, rule, msg))

    def warn(self, loc, rule, msg):
        self.warnings.append((loc, rule, msg))


def check_sentence(sent, mode, report, loc):
    limit = LIMITS[mode]
    n = count_words(sent)
    head = sent if len(sent) <= 60 else sent[:57] + "..."
    if n > 25:
        report.error(loc, "5.1/6.3", f"sentence has {n} words (max {limit}): \"{head}\"")
    elif n > 20:
        if mode == "procedural":
            report.error(loc, "5.1", f"sentence has {n} words (max 20): \"{head}\"")
        elif mode == "mixed":
            report.warn(loc, "5.1", f"sentence has {n} words (max 20 if procedural): \"{head}\"")

    if ";" in sent:
        report.error(loc, "8.1", f"semicolon found: \"{head}\". Write two sentences.")

    m = CONTRACTION.search(sent)
    if m:
        report.error(loc, "4.2", f"contraction \"{m.group(0)}\": write the full words.")

    m = HAVE_PARTICIPLE.search(sent)
    if m:
        report.error(loc, "3.4", f"helping verb structure \"{m.group(0)}\": use the simple past tense.")

    m = COMPLEX_PASSIVE.search(sent)
    if m:
        report.error(loc, "3.4", f"complex passive \"{m.group(0)}\": make the sentence active.")

    m = PASSIVE_BY.search(sent)
    if m:
        report.error(loc, "3.6", f"passive voice \"{m.group(0)}\": make the agent the subject.")
    else:
        m = PAST_PASSIVE.search(sent)
        if m:
            report.warn(loc, "3.6", f"possible passive voice \"{m.group(0)}\": make the agent the subject.")

    m = BE_ING.search(sent)
    if m:
        tail = m.group(0).split()[-1].lower()
        if tail not in ING_APPROVED:
            report.error(loc, "3.5", f"progressive form \"{m.group(0)}\": use a simple tense.")

    for word in re.findall(r"[A-Za-z-]+", sent):
        lw = word.lower()
        if lw in BANNED_MODALS:
            report.error(
                loc, "3.2",
                f"\"{word}\" is not approved. Use \"must\" (requirement), \"can\" "
                f"(possibility), \"will\" (future), or remove it.",
            )
        elif lw == "could":
            report.warn(loc, "3.2", "\"could\" is approved only as the past tense of \"can\".")
        elif lw.endswith("ing") and len(lw) > 4 and not word.isupper():
            if lw not in ING_APPROVED and lw not in ING_NOT_SUFFIX:
                report.warn(
                    loc, "3.5",
                    f"\"{word}\": an \"-ing\" form is permitted only in a technical name.",
                )


def check_vocab(text, report, approved):
    for word in re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", text):
        if word.isupper() or any(c.isupper() for c in word[1:]):
            continue  # acronym, identifier, or quoted text
        lw = word.lower()
        if lw in approved or lw in ING_APPROVED or lw in VOCAB_EXTRA or len(lw) <= 1:
            continue
        if all(p in approved for p in lw.split("-") if p):
            continue
        report.unknown[lw] = report.unknown.get(lw, 0) + 1


def check_paragraph(par, mode, report, loc, approved):
    sents = list(iter_sentences(par))
    if len(sents) > 6:
        report.error(loc, "6.6", f"paragraph has {len(sents)} sentences (max 6).")
    for s in sents:
        check_sentence(s, mode, report, loc)
    if approved:
        check_vocab(par, report, approved)


def check_text(text, mode, report, name, approved):
    text = strip_markdown(text)
    paragraphs = re.split(r"\n\s*\n", text)
    for i, par in enumerate(paragraphs):
        # a heading or a table row is a title or quoted text (rule 8.6).
        # Skip only that line. The text below a heading is still checked.
        lines = [l for l in par.splitlines()
                 if l.strip() and not l.lstrip().startswith(("#", "|"))]
        if not lines or not WORDISH.search(" ".join(lines)):
            continue
        bullet = re.compile(r"\s*(?:[-*+]|\d+\.)\s")
        items = [l for l in lines if bullet.match(l)]
        prose = [l for l in lines if not bullet.match(l)]
        # a list item counts as its own sentence (rule 8.4)
        for l in items:
            item = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", l)
            for s in iter_sentences(item):
                check_sentence(s, mode, report, f"{name}:list")
            if approved:
                check_vocab(item, report, approved)
        if prose:
            check_paragraph("\n".join(prose), mode, report, f"{name}:par{i + 1}", approved)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Check text against the STE writing rules.")
    ap.add_argument("files", nargs="*", help="files to check (default: stdin)")
    ap.add_argument("--mode", choices=["procedural", "descriptive", "mixed"],
                    default="mixed", help="text type (default: mixed)")
    ap.add_argument("--word-list", default=None,
                    help="path to word-list.md (default: ../references/word-list.md)")
    ap.add_argument("--no-vocab", action="store_true",
                    help="do not check words against the approved word list")
    ap.add_argument("--allow", action="append", default=[], metavar="FILE",
                    help="file of permitted technical names, one on each line "
                         "(default: .ste-allow in the working directory, if it exists)")
    args = ap.parse_args()

    approved = None
    if not args.no_vocab:
        wl = args.word_list
        if wl is None:
            default = Path(__file__).resolve().parent.parent / "references" / "word-list.md"
            wl = default if default.exists() else None
        if wl:
            approved = load_word_list(wl)
            allow_files = args.allow or [f for f in [".ste-allow"] if Path(f).exists()]
            for f in allow_files:
                approved |= load_allow_list(f)

    report = Report()
    if args.files:
        for f in args.files:
            check_text(Path(f).read_text(encoding="utf-8"), args.mode, report, f, approved)
    else:
        check_text(sys.stdin.read(), args.mode, report, "stdin", approved)

    for loc, rule, msg in report.errors:
        print(f"ERROR   {loc} [rule {rule}] {msg}")
    for loc, rule, msg in report.warnings:
        print(f"WARNING {loc} [rule {rule}] {msg}")
    if report.unknown:
        words = sorted(report.unknown, key=report.unknown.get, reverse=True)
        print(f"\nCHECK   {len(words)} words are not in the approved word list.")
        print("        Each must be an approved technical name or technical verb:")
        for chunk in [words[i:i + 10] for i in range(0, len(words), 10)]:
            print("        " + ", ".join(chunk))

    print(f"\nResult: {len(report.errors)} errors, {len(report.warnings)} warnings.")
    if not report.errors:
        print("The text obeys the STE structural rules that this tool can check.")
        print("This tool cannot make sure that each word has its approved meaning.")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
