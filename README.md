# Simplified Technical English skill

This skill makes an LLM write in Simplified Technical English (STE).
STE is a controlled language for technical documentation.
The specification ASD-STE100 defines STE.
Text in STE is clear, short, and easy to translate.

## Contents

- `SKILL.md` — the primary instructions for the LLM
- `references/writing-rules.md` — the 53 writing rules, with examples
- `references/word-list.md` — the 869 approved words
- `references/substitutions.md` — replacements for frequent unapproved words
- `examples/before-after.md` — examples of text before and after the change
- `scripts/ste_check.py` — a check tool for the rules that a script can find
- `NOTICE.md` — copyright information

## How to use this skill with Claude

1. Copy this folder to `~/.claude/skills/simplified-technical-english/`:

       git clone https://github.com/0xpili/simplified-technical-english.git ~/.claude/skills/simplified-technical-english

2. Ask Claude to write or check technical text in STE.
3. Claude finds the skill and obeys the rules.

You can also start the skill directly. Type `/simplified-technical-english`.

## How to use this skill with a different LLM

1. Open `SKILL.md` and copy its text into the system prompt.
2. If the LLM accepts more text, add `references/substitutions.md`.
3. For the best results, also add `references/word-list.md`.
4. Ask the LLM to write technical text.

## How to check a text

Run the check tool on a file or on standard input:

    python3 scripts/ste_check.py --mode procedural draft.txt
    python3 scripts/ste_check.py --mode descriptive chapter.md

The tool needs only Python 3. The tool shows each error and its rule number.
The tool cannot find all the errors.
A person who knows STE must also examine the text.

## Source

The source of this skill is ASD-STE100 Issue 7 (2017).
You can get the official specification free of charge from https://www.asd-ste100.org.
This skill is not an official ASD document. Refer to `NOTICE.md`.
