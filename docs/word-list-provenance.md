# The source and the legal status of the word list

This file gives the source of the approved word list, its legal status, and the options to publish it.

## Source

`references/word-list.md` shows words from the dictionary of ASD-STE100 (Issue 7, 2017).
Each line gives one word, its part of speech, and its approved forms.

The list does not give the approved meanings, the definitions, or the examples of the dictionary.

## Word count

The list has 869 entries.

One entry uses a Unicode ellipsis character in the headword. This is the conjunction `AS ... AS`.
The parser in `scripts/ste_check.py` does not read this entry. Thus the checker loads 868 entries.
This is a known issue.

## Counting method

Count the lines that agree with the format `WORD (part of speech)`.
The plurals of countable nouns are not separate entries.

## Legal status

ASD-STE100 is the property of ASD (AeroSpace and Defence Industries Association of Europe), Brussels, Belgium.
ASD-STE100 is a registered trade mark of ASD (European Union Trade Mark No. 017966390).

This skill is not an official ASD product. ASD did not approve this skill and does not endorse it.

## Redistribution

The word list shows dictionary words, their parts of speech, and their forms.
It does not show the definitions or the examples.

Before you use or publish this list, make sure that the conditions of ASD permit it. You have these options:

1. Ask ASD for written permission.
2. Do not put the list in the repository. Build the list from your own copy of the official specification.
3. Keep only a small example of the list.

Refer to `NOTICE.md` for more data.
