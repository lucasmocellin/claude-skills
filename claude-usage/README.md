# claude-usage

A Claude Code skill that generates a **weekly usage report** by parsing your local session files — no API calls, no external services.

## What it shows

```
Claude Code Usage — Week of Mar 23 – Mar 29, 2026

┌────────────┬──────────┬───────┬───────┬─────────┬────────────┬────────────┐
│ Date       │ Sessions │ Turns │ Tools │ Runtime │ Out tokens │ Cache read │
├────────────┼──────────┼───────┼───────┼─────────┼────────────┼────────────┤
│ Mon Mar 23 │       17 │   346 │   240 │  2h 29m │     106.5K │      23.0M │
│ Tue Mar 24 │        9 │   168 │   113 │     46m │      46.5K │      11.4M │
│ Wed Mar 25 │        9 │   197 │   158 │  1h 25m │      73.3K │      14.8M │
│ Thu Mar 26 │        5 │   139 │   117 │  1h 08m │      96.7K │      12.9M │
│ Fri Mar 27 │        2 │    88 │    63 │     33m │      45.4K │       4.8M │
│ Sat Mar 28 │        — │     — │     — │       — │          — │          — │
│ Sun Mar 29 │        — │     — │     — │       — │          — │          — │
├────────────┼──────────┼───────┼───────┼─────────┼────────────┼────────────┤
│ TOTAL      │       42 │   938 │   691 │  6h 21m │     368.5K │      66.9M │
└────────────┴──────────┴───────┴───────┴─────────┴────────────┴────────────┘
```

Followed by a per-session breakdown for each day with project, runtime, turns, tools used, and first prompt.

**Runtime** is active time — consecutive message gaps > 15 min are excluded, so idle time and remote-control sessions don't inflate the numbers.

## Install

```bash
git clone https://github.com/lucasmocellin/claude-skills ~/git/claude-skills
ln -s ~/git/claude-skills/claude-usage ~/.claude/skills/claude-usage
```

## Usage

In any Claude Code session:

```
/claude-usage           → this week (Mon–Sun)
/claude-usage 7d        → rolling last 7 days
/claude-usage 2026-03-25 → single day
```

## Requirements

- Claude Code
- Python 3 (stdlib only, no dependencies)
- macOS or Linux
