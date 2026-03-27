# claude-skills

A collection of Claude Code skills by [@lucasmocellin](https://github.com/lucasmocellin).

## Install

```bash
git clone https://github.com/lucasmocellin/claude-skills ~/.claude/skills/
```

That's it. All skills are immediately available as slash commands.

If your Claude skills folder is in a different location, replace `~/.claude/skills/` in the command above with your path.

Updates: `cd ~/.claude/skills && git pull`

## Skills

| Skill | Description |
|-------|-------------|
| [claude-usage](./claude-usage) | Weekly usage report for Claude Code — sessions, runtime, turns, tokens |

## Adding skills

Each skill is a folder with a `SKILL.md` at its root. The folder name becomes the slash command (e.g. `claude-usage/` → `/claude-usage`).
