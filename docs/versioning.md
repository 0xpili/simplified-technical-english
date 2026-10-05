# Versioning

This file tells you which issue of ASD-STE100 the skill obeys, and how to upgrade the skill.

## The specification

This skill is based on ASD-STE100 Issue 7 (2017-01-25).

ASD releases new issues. At the date of this file, the current issue is Issue 9 (2025-01-15).
You can get the official specification free of charge from https://www.asd-ste100.org.

The skill can be different from the current issue. Always compare the skill with the official specification before you use it for important work.

## The skill version

The skill obeys Semantic Versioning (MAJOR.MINOR.PATCH):

- MAJOR: a change to a rule, or a change to the approved word list.
- MINOR: new text or a new tool. The existing rules do not change.
- PATCH: a correction that does not change a rule or the word list.

The current version is 0.1.0. A version below 1.0.0 shows that the skill is not complete.

## Files that give the issue

These files give the source issue:

- `SKILL.md`, in the `metadata.source-specification` field.
- `references/word-list.md`.
- `references/writing-rules.md`.
- `NOTICE.md`.

## How to upgrade to a new issue

Do these steps:

1. Get the new official specification.
2. Compare the new rules with `references/writing-rules.md`. Change the rules that are different.
3. Compare the new dictionary with `references/word-list.md`. Add and remove words.
4. Change the issue number in the four files above.
5. Change `scripts/ste_check.py` if a rule changed.
6. Add the change to `CHANGELOG.md`.
7. Do a check of `README.md` and of the examples.

## Important limitation

This skill is not an official ASD document. It cannot make sure that your text obeys ASD-STE100. Refer to `NOTICE.md`.
