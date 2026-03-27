#!/usr/bin/env python3
"""
Claude Code weekly usage report.
Usage:
  python3 report.py            # last 7 days
  python3 report.py YYYY-MM-DD # single day
  python3 report.py week       # Mon–Sun of current week
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, date, timedelta


# ── Date range ────────────────────────────────────────────────────────────────

arg = sys.argv[1] if len(sys.argv) > 1 else 'week'

if arg == 'week':
    today = date.today()
    start = today - timedelta(days=today.weekday())       # Monday
    end   = start + timedelta(days=6)                     # Sunday
    label = f'Week of {start.strftime("%b %d")} – {end.strftime("%b %d, %Y")}'
elif arg == '7d':
    end   = date.today()
    start = end - timedelta(days=6)
    label = f'Last 7 days ({start.strftime("%b %d")} – {end.strftime("%b %d")})'
else:
    # Single day
    start = end = date.fromisoformat(arg)
    label = start.strftime('%A, %b %d %Y')

date_range = set(
    (start + timedelta(days=i)).isoformat()
    for i in range((end - start).days + 1)
)

# ── Parse sessions ─────────────────────────────────────────────────────────────

base      = os.path.expanduser('~/.claude/projects')
home_slug = '-' + os.path.expanduser('~').replace('/', '-').lstrip('-')

all_sessions = []   # (file_dt, proj_dir, sid, fpath, iso_date)
for proj_dir in os.listdir(base):
    proj_path = os.path.join(base, proj_dir)
    if not os.path.isdir(proj_path):
        continue
    for f in os.listdir(proj_path):
        if not f.endswith('.jsonl'):
            continue
        fpath = os.path.join(proj_path, f)
        mtime = os.path.getmtime(fpath)
        dt    = datetime.fromtimestamp(mtime)
        iso   = dt.strftime('%Y-%m-%d')
        if iso in date_range:
            all_sessions.append((dt, proj_dir, f.replace('.jsonl', ''), fpath, iso))

all_sessions.sort()


def parse_session(fpath):
    with open(fpath) as f:
        lines = f.readlines()

    msg_timestamps, user_turns, input_tok, output_tok = [], 0, 0, 0
    cache_read, cache_write, task_count, tool_count = 0, 0, 0, 0
    first_prompt = None

    for line in lines:
        try:
            msg = json.loads(line)
        except Exception:
            continue
        t  = msg.get('type')
        ts = msg.get('timestamp')
        if ts:
            msg_timestamps.append(ts)

        if t == 'user' and not msg.get('isSidechain'):
            user_turns += 1
            if first_prompt is None:
                content = msg.get('message', {}).get('content', '')
                if isinstance(content, list):
                    for part in content:
                        if isinstance(part, dict) and part.get('type') == 'text':
                            first_prompt = part.get('text', '')[:60]
                            break
                elif isinstance(content, str):
                    first_prompt = content[:60]

        elif t == 'assistant':
            usage = msg.get('message', {}).get('usage', {})
            input_tok   += usage.get('input_tokens', 0)
            output_tok  += usage.get('output_tokens', 0)
            cache_read  += usage.get('cache_read_input_tokens', 0)
            cache_write += usage.get('cache_creation_input_tokens', 0)
            for item in msg.get('message', {}).get('content', []):
                if isinstance(item, dict) and item.get('type') == 'tool_use':
                    tool_count += 1
                    if item.get('name') == 'TaskCreate':
                        task_count += 1

    # Active runtime: sum consecutive gaps ≤ 15 min
    runtime_min = None
    if len(msg_timestamps) >= 2:
        try:
            active_secs = 0
            parsed = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in msg_timestamps]
            for i in range(1, len(parsed)):
                gap = (parsed[i] - parsed[i - 1]).total_seconds()
                if gap <= 900:
                    active_secs += gap
            runtime_min = int(active_secs / 60)
        except Exception:
            pass

    return {
        'turns':        user_turns,
        'tools':        tool_count,
        'tasks':        task_count,
        'input_tok':    input_tok,
        'output_tok':   output_tok,
        'cache_read':   cache_read,
        'runtime_min':  runtime_min,
        'first_prompt': (first_prompt or '').replace('\n', ' '),
    }


def shorten_proj(proj):
    return (
        proj
        .replace(home_slug + '-git-hubstaff-', 'hs/')
        .replace(home_slug + '-git-', 'git/')
        .replace(home_slug, '~')
    )


def fmt_tok(n):
    if n >= 1_000_000:
        return f'{n / 1_000_000:.1f}M'
    if n >= 1_000:
        return f'{n / 1_000:.1f}K'
    return str(n)


def fmt_runtime(minutes):
    if minutes is None:
        return '—'
    if minutes >= 60:
        h, m = divmod(minutes, 60)
        return f'{h}h {m:02d}m'
    return f'{minutes}m'


# ── Box-drawing table ──────────────────────────────────────────────────────────

def table(headers, rows, aligns=None):
    """
    headers: list of str
    rows:    list of list of str  (last row = totals if you want a separator)
    aligns:  list of '<' or '>'  (default all left)
    """
    aligns = aligns or ['<'] * len(headers)
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    def bar(left, mid, right, fill='─'):
        return left + fill + (fill + mid + fill).join(fill * w for w in widths) + fill + right

    def row_line(cells, sep='│'):
        parts = []
        for i, cell in enumerate(cells):
            w = widths[i]
            s = str(cell)
            parts.append(f' {s:{aligns[i]}{w}} ')
        return sep + sep.join(parts) + sep

    lines = [
        bar('┌', '┬', '┐'),
        row_line(headers),
        bar('├', '┼', '┤'),
    ]
    for i, row in enumerate(rows):
        if i == len(rows) - 1 and getattr(rows, '_has_total', False):
            lines.append(bar('├', '┼', '┤'))
        lines.append(row_line(row))
    lines.append(bar('└', '┴', '┘'))
    return '\n'.join(lines)


# ── Build data ─────────────────────────────────────────────────────────────────

by_day     = defaultdict(list)   # iso_date -> list of session dicts
day_totals = defaultdict(lambda: dict(sessions=0, turns=0, tools=0, tasks=0,
                                      output_tok=0, cache_read=0, runtime_min=0))

for file_dt, proj_dir, sid, fpath, iso in all_sessions:
    s = parse_session(fpath)
    s['time']    = file_dt.strftime('%H:%M')
    s['project'] = shorten_proj(proj_dir)
    by_day[iso].append(s)

    d = day_totals[iso]
    d['sessions']   += 1
    d['turns']      += s['turns']
    d['tools']      += s['tools']
    d['tasks']      += s['tasks']
    d['output_tok'] += s['output_tok']
    d['cache_read'] += s['cache_read']
    if s['runtime_min'] is not None:
        d['runtime_min'] += s['runtime_min']

# ── Print ──────────────────────────────────────────────────────────────────────

print(f'\nClaude Code Usage — {label}\n')

# Weekly summary table
if len(date_range) > 1:
    sum_headers = ['Date', 'Sessions', 'Turns', 'Tools', 'Runtime', 'Out tokens', 'Cache read']
    sum_aligns  = ['<',    '>',        '>',     '>',     '>',       '>',          '>']
    sum_rows    = []
    grand = dict(sessions=0, turns=0, tools=0, tasks=0, output_tok=0, cache_read=0, runtime_min=0)

    for iso in sorted(date_range):
        d = day_totals[iso]
        day_label = datetime.fromisoformat(iso).strftime('%a %b %d')
        if d['sessions'] == 0:
            sum_rows.append([day_label, '—', '—', '—', '—', '—', '—'])
        else:
            sum_rows.append([
                day_label,
                str(d['sessions']),
                str(d['turns']),
                str(d['tools']),
                fmt_runtime(d['runtime_min']),
                fmt_tok(d['output_tok']),
                fmt_tok(d['cache_read']),
            ])
        for k in grand:
            grand[k] += d[k]

    # Totals row with separator
    totals_row = [
        'TOTAL',
        str(grand['sessions']),
        str(grand['turns']),
        str(grand['tools']),
        fmt_runtime(grand['runtime_min']),
        fmt_tok(grand['output_tok']),
        fmt_tok(grand['cache_read']),
    ]

    # Print summary with manual totals separator
    headers = sum_headers
    aligns  = sum_aligns
    widths  = [len(h) for h in headers]
    for row in sum_rows + [totals_row]:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    def bar(l, m, r, fill='─'):
        return l + fill + (fill + m + fill).join(fill * w for w in widths) + fill + r

    def rline(cells, sep='│'):
        parts = [f' {str(c):{aligns[i]}{widths[i]}} ' for i, c in enumerate(cells)]
        return sep + sep.join(parts) + sep

    print(bar('┌', '┬', '┐'))
    print(rline(headers))
    print(bar('├', '┼', '┤'))
    for row in sum_rows:
        print(rline(row))
    print(bar('├', '┼', '┤'))
    print(rline(totals_row))
    print(bar('└', '┴', '┘'))
    print()

# Per-day session breakdown
sess_headers = ['Time', 'Project', 'Runtime', 'Turns', 'Tools', 'Out tok', 'First prompt']
sess_aligns  = ['<',    '<',       '>',       '>',     '>',     '>',       '<']

for iso in sorted(date_range):
    sessions = by_day.get(iso)
    if not sessions:
        continue

    day_label = datetime.fromisoformat(iso).strftime('%A, %b %d')
    print(f'{day_label}')

    col_proj = max(7, max(len(s['project']) for s in sessions))
    col_fp   = 35

    sess_rows = []
    for s in sessions:
        fp = s['first_prompt'][:col_fp] + ('…' if len(s['first_prompt']) > col_fp else '')
        sess_rows.append([
            s['time'],
            s['project'],
            fmt_runtime(s['runtime_min']),
            str(s['turns']),
            str(s['tools']),
            fmt_tok(s['output_tok']),
            fp,
        ])

    # Compute widths
    all_rows = [sess_headers] + sess_rows
    widths = [len(h) for h in sess_headers]
    for row in sess_rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    def bar2(l, m, r, fill='─'):
        return l + fill + (fill + m + fill).join(fill * w for w in widths) + fill + r

    def rline2(cells, sep='│'):
        parts = [f' {str(c):{sess_aligns[i]}{widths[i]}} ' for i, c in enumerate(cells)]
        return sep + sep.join(parts) + sep

    print(bar2('┌', '┬', '┐'))
    print(rline2(sess_headers))
    print(bar2('├', '┼', '┤'))
    for row in sess_rows:
        print(rline2(row))
    print(bar2('└', '┴', '┘'))
    print()
