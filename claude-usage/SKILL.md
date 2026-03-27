---
name: claude-usage
description: Report Claude Code session usage for today (or a given date). Shows sessions, turns, runtime, tool calls, and token usage. Use when the user says "/claude-usage", "how many sessions today", "show my Claude usage", "how much have I used Claude today", or asks about session stats, runtime, or token usage for Claude Code.
---

# Claude Usage Report

Generate a daily usage report by parsing local Claude Code session files in `~/.claude/projects/`.

## Inputs

- **No argument** — current week (Mon–Sun), default
- **`7d`** — rolling last 7 days
- **`YYYY-MM-DD`** — single day (e.g. `2026-03-25`, "yesterday", "March 25")

## Instructions

Run the script via the Bash tool.

```bash
# This week (default)
python3 {SKILL_DIR}/scripts/report.py

# Rolling 7 days
python3 {SKILL_DIR}/scripts/report.py 7d

# Single day — resolve the date to ISO format first
python3 {SKILL_DIR}/scripts/report.py 2026-03-25
```

The `{SKILL_DIR}` placeholder resolves to the skill's base directory shown at the top of this file.

## Output

Present the output as-is from the script. Then add a one-sentence insight if anything stands out (e.g. longest session, most tool-heavy session, unusually high cache usage).

## Notes

- **Runtime** is *active time* — sum of consecutive message intervals ≤ 15 min. Idle gaps (user away, remote sessions waiting) are excluded. This gives real working time even for remote-control sessions.
- **Cache read** is usually much larger than fresh input — this is normal for long sessions with large context.
- **Tasks** counts `TaskCreate` tool calls specifically.
- **Tools** counts all tool use calls (Bash, Read, Edit, MCP tools, etc.).
- The report uses file modification time to determine session date, and also as the session "start time" for the Time column (approximation).
