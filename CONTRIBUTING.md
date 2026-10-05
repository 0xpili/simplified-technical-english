# Contributing

Thank you for your help with this skill.

This file tells you how to contribute.

## What you can contribute

- A correction to a rule in `references/writing-rules.md`.
- A change to the approved word list in `references/word-list.md`.
- A replacement in `references/substitutions.md`.
- An example in `examples/before-after.md`.
- A correction to `scripts/ste_check.py`.
- A correction to the documentation.

## Before you start

- Use Python 3.9 or later.
- Write your text in STE. The skill obeys the rules that it gives. This file is in STE.
- Do not add the definitions or the examples of the ASD-STE100 dictionary. The dictionary is the property of ASD. Refer to `docs/word-list-provenance.md`.

## Run the checker

Run the checker on a file that you changed:

    python3 scripts/ste_check.py --mode descriptive README.md
    python3 scripts/ste_check.py --mode procedural draft.txt

The checker gives an exit code of 1 when it finds an error.

## Run the tests

The tests use only the Python standard library:

    python3 -m unittest discover tests

The test suite comes with the checker improvements. If the `tests` directory is not in your copy, this command does nothing.

## Add or change an approved word

The word list is a copy of the words in the official specification. Obey these rules:

- Use the format `WORD (part of speech) [approved forms]`.
- Put the entries in alphabetical order.
- Add a word only when the official specification has it.
- Do not add a definition, a meaning, or an example.
- Give the source issue in your pull request.

## Report a problem with the checker

Open an issue and give this data:

- The input text.
- The command that you used.
- The result that you expected.
- The result that you obtained.

## Commit messages

Use the Conventional Commits format. Examples:

- `docs: add a versioning policy`
- `fix: correct a false passive result`

## License

Refer to `LICENSE` and `NOTICE.md`.

Your contribution uses the MIT license. The word list stays the property of ASD.
