# claude-skills

A collection of Claude Code skills by [@lucasmocellin](https://github.com/lucasmocellin).

## Install

```bash
git clone https://github.com/lucasmocellin/claude-skills ~/.claude/skills/
```

That's it. All skills are immediately available as slash commands.

> **Already have a `~/.claude/skills/` directory?**
> Move your existing skills into the repo folder first, then make it a git repo — or clone elsewhere and set `skillsDirectory` in your Claude Code settings to point to it:
> ```json
> // ~/.claude/settings.json
> { "skillsDirectory": "~/git/claude-skills" }
> ```

Updates: `cd ~/.claude/skills && git pull`

## Skills

| Skill | Description |
|-------|-------------|
| [claude-usage](./claude-usage) | Weekly usage report for Claude Code — sessions, runtime, turns, tokens |

## Adding skills

Each skill is a folder with a `SKILL.md` at its root. The folder name becomes the slash command (e.g. `claude-usage/` → `/claude-usage`).
