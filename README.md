# claude-skills

A collection of Claude Code skills by [@lucasmocellin](https://github.com/lucasmocellin).

## Install

Install any skill directly into your skills folder:

```bash
curl -fsSL https://github.com/lucasmocellin/claude-skills/archive/refs/heads/main.tar.gz | tar -xz --strip-components=1 -C ~/.claude/skills/ claude-skills-main/claude-usage
```

Replace `claude-usage` with any other skill name from this repo. Run the same command again to update.

## Skills

| Skill | Description |
|-------|-------------|
| [claude-usage](./claude-usage) | Weekly usage report for Claude Code — sessions, runtime, turns, tokens |

## Adding skills

Each skill is a folder with a `SKILL.md` at its root. The folder name becomes the slash command (e.g. `claude-usage/` → `/claude-usage`).
