---
name: simplified-technical-english
description: Writes and rewrites text in Simplified Technical English (ASD-STE100), a controlled language for clear technical documentation. Use when the user asks for STE, Simplified Technical English, controlled language, or plain technical writing, and when the user asks to write, rewrite, review, or check technical documentation, procedures, manuals, instructions, warnings, or reports.
license: MIT for the text of this skill. The word list in references/word-list.md comes from the ASD-STE100 dictionary, which is the property of ASD. Refer to NOTICE.md.
metadata:
  source-specification: ASD-STE100 Issue 7 (2017-01-25)
---

# Simplified Technical English

This skill makes you write in Simplified Technical English (STE).
STE is a controlled language for technical documentation.
The specification ASD-STE100 gives 53 writing rules and a dictionary of approved words.
Text in STE is clear to readers who do not know much English.

Obey the rules in this file for all the technical text that you write.
The rules in this file are the most important rules.
The full set of rules is in `references/writing-rules.md`.
The approved words are in `references/word-list.md`.

## Scope

Apply STE to technical output: documentation, procedures, manuals, instructions, reports, error messages, and answers about technical subjects.

Do not apply STE to:

- Marketing text or brand text
- Poems, stories, or conversation
- Code blocks, identifiers, commands, file paths, and quoted error messages
- Quoted text and official names of products, parts, and documents.

If the user asks for a different style, the request of the user wins.

## Step 1: Classify the text

Before you write, classify each part of the text:

- **Procedural text** tells the reader to do something. Example: "Remove the four bolts."
- **Descriptive text** gives information. Example: "The pump supplies fuel to the engine."

The two types have different limits. Do not mix the two types in one paragraph.

## Step 2: Obey the verb rules

- Use only these verb forms: infinitive, imperative, simple present, simple past, future with "will", and past participle as an adjective.
- Do not use the "-ing" form of a verb. Approved "-ing" words are only: mating, missing, remaining, lighting, opening, routing, servicing, during.
- Do not use a helping verb with a past participle. Write "the operator adjusted the linkage", not "the operator has adjusted the linkage".
- Use the active voice. Write "a relay connects the circuits", not "the circuits are connected by a relay".
- In procedures, use the imperative. Write "Set the switch to ON."
- If there is no agent, use "you" or "we" as the subject.
- Use only "can", "must", and "will" as helping verbs. Do not use "should", "would", "may", "might", or "shall".
- A past participle after "is" or "are" shows a condition and is permitted. "The wires are disconnected."

## Step 3: Obey the sentence rules

- Procedural sentences: maximum 20 words.
- Descriptive sentences: maximum 25 words.
- Paragraphs: maximum 6 sentences, and only one topic.
- Write only one instruction in each sentence. Two actions are permitted only when they occur at the same time.
- Write only one topic in each sentence.
- When a condition comes before a command, put a comma after the condition. "If the light comes on, stop the engine."
- Keep the articles, the subjects, the verbs, and the conjunction "that". Write "make sure that the file exists".
- Do not use contractions. Write "do not", not "don't".
- Do not use semicolons. Write two sentences.
- Use a vertical list for complex text. In a list of commands with "not", write "not" again in each item.

## Step 4: Obey the word rules

- Use only: approved words from `references/word-list.md`, technical names, and technical verbs.
- A technical name is the official name of a part, tool, material, system, document, or term of your subject. Examples: "engine", "firewall", "torque wrench", "SKILL.md".
- Use an approved word only as its given part of speech. "Test" is a noun, not a verb. Write "do a test", not "test the system".
- Use one name for one item in the full text. Do not change between names for the same item.
- Write noun clusters of maximum three words. Break long clusters with "of", "on", "in", or "for".
- Do not make phrasal verbs. Write "extinguish the fire", not "put out the fire".
- Do not use vague words. Write the specific quantity, name, or action.
- Use American English spelling.
- Common replacements are in `references/substitutions.md`.

## Step 5: Write safety instructions correctly

- Use "WARNING" for a risk of injury or death to persons.
- Use "CAUTION" for a risk of damage to objects.
- Start with a simple command or condition. Then give the risk.
- Example: "WARNING: Do not touch the connector. The connector can have a dangerous voltage."

## Step 6: Check your text

After you write, check your text. Do these steps:

1. If you can run scripts, run: `python3 scripts/ste_check.py --mode <procedural|descriptive> <file>`.
2. If you cannot run scripts, do a manual scan of the checklist below.
3. Correct each error.
4. Check the text again. Stop only when the text has no errors.

Manual scan checklist:

- Find semicolons and contractions. Remove them.
- Find "has", "have", and "had" before a past participle. Use the simple past tense.
- Find "should", "would", "may", "might", and "shall". Replace them or remove them.
- Find "-ing" words that are not approved and are not in technical names. Rewrite them.
- Find passive voice. Make the agent the subject, or use the imperative.
- Count the words in the longest sentences. Divide sentences that are too long.
- Count the sentences in each paragraph. Divide paragraphs that have more than 6 sentences.
- Find words that are not approved and are not technical names. Replace them.

The check tool cannot find all the errors.
The tool cannot know if a word has its approved meaning.
You must also compare your words with `references/word-list.md`.

## Reference files

- `references/writing-rules.md` — all 53 rules and 4 recommendations, with examples. Read this file when you rewrite a document or when a rule is not clear.
- `references/word-list.md` — the 869 approved words with their parts of speech and forms.
- `references/substitutions.md` — replacements for frequent unapproved words, and the categories of technical names and technical verbs.
- `examples/before-after.md` — examples of text before and after the change to STE.

## Basis

The source of this skill is ASD-STE100 Issue 7 (2017).
ASD releases new issues of the specification.
You can get the specification free of charge from https://www.asd-ste100.org.
This skill is not an official ASD document.
This skill cannot make sure that your text obeys the official specification fully.
Refer to NOTICE.md for the copyright information.
