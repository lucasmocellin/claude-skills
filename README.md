# claude-skills

A collection of Claude Code skills by [@lucasmocellin](https://github.com/lucasmocellin).

## Install

**New install** (no existing `~/.claude/skills/` directory):
```bash
git clone https://github.com/lucasmocellin/claude-skills ~/.claude/skills/
```

**Already have a skills directory** — symlink individual skills instead:
```bash
git clone https://github.com/lucasmocellin/claude-skills ~/git/claude-skills
ln -s ~/git/claude-skills/claude-usage ~/.claude/skills/claude-usage
```

All skills are immediately available as slash commands after install.

Updates: `cd ~/.claude/skills && git pull` (or `~/git/claude-skills` if you used the symlink path)

## Skills

| Skill | Description |
|-------|-------------|
| [claude-usage](./claude-usage) | Weekly usage report for Claude Code — sessions, runtime, turns, tokens |

## Adding skills

Each skill is a folder with a `SKILL.md` at its root. The folder name becomes the slash command (e.g. `claude-usage/` → `/claude-usage`).
