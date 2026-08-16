# Simplified Technical English skill

This skill makes an LLM write in Simplified Technical English (STE).
STE is a controlled language for technical documentation.
The specification ASD-STE100 gives the rules of STE and its dictionary.
The aerospace and defense industries use STE for their manuals.
Text in STE is clear, short, and easy to translate.

The skill obeys the rules that it gives. This README is in STE.

## Example

Text before the change:

> Prior to commencing the installation, it should be ensured that all
> components have been thoroughly inspected for damage.

Text after the change:

> Before you start the installation, examine all the components for damage.

## Contents of this repository

| File | Function |
|---|---|
| `SKILL.md` | The primary instructions for the LLM |
| `references/writing-rules.md` | The 53 writing rules, with examples |
| `references/word-list.md` | The 869 approved words |
| `references/substitutions.md` | Replacements for frequent unapproved words |
| `examples/before-after.md` | Examples of text before and after the change |
| `scripts/ste_check.py` | A check tool for the STE rules |
| `NOTICE.md` | Copyright information |

## How to install the skill for Claude

1. Clone this repository into your skills folder:

       git clone https://github.com/0xpili/simplified-technical-english.git ~/.claude/skills/simplified-technical-english

2. Tell Claude to write or examine technical text in STE.
3. Claude finds the skill and obeys the rules.

You can also start the skill directly. Type `/simplified-technical-english`.

## How to use the skill with a different LLM

1. Open `SKILL.md`. Copy its text into the system prompt of the LLM.
2. If the LLM accepts more text, add the text of `references/substitutions.md`.
3. For the best results, also add the text of `references/word-list.md`.
4. Tell the LLM to write technical text.

## How to do a check of a text

Run the check tool on a file or on standard input:

    python3 scripts/ste_check.py --mode procedural draft.txt
    python3 scripts/ste_check.py --mode descriptive chapter.md

The tool finds these errors:

- Sentences that have too many words
- Paragraphs that have more than six sentences
- Verb forms that are not approved, and the passive voice
- Semicolons, contractions, and unapproved helping verbs
- Words that are not in the approved word list.

The tool uses only Python 3. The tool shows each error and its rule number.

## Limits of the skill

The tool cannot find all the errors.
The tool cannot know if a word has its approved meaning.
A person who knows STE must also examine an important text.
This skill is not an official ASD document.
This skill cannot make sure that your text obeys the official specification fully.

## Source and copyright

The source of this skill is ASD-STE100 Issue 7 (2017).
ASD releases new issues of the specification.
You can get the specification free of charge from https://www.asd-ste100.org.
The dictionary of ASD-STE100 is the property of ASD. Refer to `NOTICE.md`.
The text of this skill and its scripts have the MIT license. Refer to `LICENSE`.
