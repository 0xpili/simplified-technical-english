# How to install the skill

This skill obeys the Agent Skills standard. You can find the standard at https://agentskills.io.
An Agent Skill is a folder that contains a `SKILL.md` file and the files that the skill uses.

Many tools find a skill in a standard folder. These tools include Claude Code, OpenCode, Cursor, GitHub Copilot, OpenAI Codex, and Gemini CLI.

## Requirements

- The name of the skill folder must agree with the `name` field in `SKILL.md`. This name is `simplified-technical-english`. Always use this folder name.
- The check tool `scripts/ste_check.py` uses Python 3.9 or later.
- The skill uses `references/`, `examples/`, and `scripts/`. Keep these folders together with `SKILL.md`.

## Quick start

Clone the repository into the skills folder of your tool:

    git clone https://github.com/0xpili/simplified-technical-english.git <SKILLS_FOLDER>/simplified-technical-english

The table below gives the skills folder and the start command for each tool.

| Tool | Global skills folder | Project skills folder | Start the skill |
|---|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | `/simplified-technical-english` |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` | `@simplified-technical-english` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` | `/simplified-technical-english` |
| GitHub Copilot (VS Code) | `~/.copilot/skills/` | `.github/skills/` | `/simplified-technical-english` |
| OpenAI Codex | `~/.codex/skills/` | `.agents/skills/` | `$simplified-technical-english` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` | `/skills` |

The cross-client folder `.agents/skills/` also works in Cursor, GitHub Copilot, OpenAI Codex, Gemini CLI, and OpenCode. Use it when you want one copy of the skill for more than one tool.

## Claude Code

    git clone https://github.com/0xpili/simplified-technical-english.git ~/.claude/skills/simplified-technical-english

Claude Code finds the skill automatically.
Start the skill directly with `/simplified-technical-english`.

## OpenCode

    git clone https://github.com/0xpili/simplified-technical-english.git ~/.config/opencode/skills/simplified-technical-english

OpenCode finds a skill in `~/.config/opencode/skills` and in `.opencode/skills`.
OpenCode also finds a skill in `~/.claude/skills`, `.claude/skills`, `.agents/skills`, and `~/.agents/skills`.
Thus the Claude Code install also works in OpenCode.

Start the skill directly with `@simplified-technical-english`.

You can also give OpenCode the folder of the skill in `opencode.json`:

    {
      "skills": ["./simplified-technical-english"]
    }

## Cursor

    git clone https://github.com/0xpili/simplified-technical-english.git ~/.cursor/skills/simplified-technical-english

Cursor finds the skill automatically. Refer to the Cursor menu Settings > Rules > Agent Decides.
Start the skill directly with `/simplified-technical-english`.

## GitHub Copilot in VS Code

    git clone https://github.com/0xpili/simplified-technical-english.git ~/.copilot/skills/simplified-technical-english

Copilot finds the skill automatically.
Start the skill directly with `/simplified-technical-english`.

## OpenAI Codex

    git clone https://github.com/0xpili/simplified-technical-english.git ~/.codex/skills/simplified-technical-english

Codex finds the skill automatically.
Start the skill directly with `$simplified-technical-english`.

## Gemini CLI

    gemini skills install https://github.com/0xpili/simplified-technical-english.git --consent

Gemini CLI asks for consent before it uses the skill.
Use `/skills list` to show the skills that Gemini CLI found.

## Tools without skills

If your tool does not have skills, copy the text of `SKILL.md` into the system prompt or the instructions file of the tool.
If the tool accepts more text, also add `references/substitutions.md` and `references/word-list.md`.
Then tell the tool to write technical text.

## Notes

- The check tool uses the path of the skill folder. Run it from the skill folder:

      python3 scripts/ste_check.py --mode descriptive README.md

- This skill is not an official ASD document. Refer to `NOTICE.md`.
- If a tool does not find the skill, do the troubleshooting steps of that tool. The usual cause is the folder name or the `description` field.
