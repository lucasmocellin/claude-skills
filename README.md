# claude-skills

A collection of Claude Code skills by [@lucasmocellin](https://github.com/lucasmocellin).

## Install

```bash
git clone https://github.com/lucasmocellin/claude-skills ~/git/claude-skills
```

Then symlink whichever skills you want:

```bash
ln -s ~/git/claude-skills/claude-usage ~/.claude/skills/claude-usage
```

Updates are automatic — just `git pull` to get the latest.

## Skills

| Skill | Description |
|-------|-------------|
| [claude-usage](./claude-usage) | Weekly usage report for Claude Code — sessions, runtime, turns, tokens |

## Adding skills

Each skill is a folder with a `SKILL.md` at its root. The folder name becomes the slash command (e.g. `claude-usage/` → `/claude-usage`).
