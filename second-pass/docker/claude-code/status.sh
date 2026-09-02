#!/usr/bin/env bash
# status.sh — live progress of the benchmark matrix.
# One-shot report; use `watch -n 30 ./status.sh` for a live view.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"

running=$(docker ps --filter ancestor=humaneval-claude-runner --format '{{.ID}}' 2>/dev/null | wc -l)
echo "=== $(date '+%H:%M:%S')  |  running containers: $running ==="

python3 - "$REPO" <<'PY'
import json, os, sys, glob, time
repo = sys.argv[1]
rows, done, total = [], 0, 0
for cfg in sorted(os.listdir(f'{repo}/runs')):
    if cfg == 'archive' or cfg.startswith('.'): continue
    cdir = f'{repo}/runs/{cfg}'
    if not os.path.isdir(cdir): continue
    probs = sorted(os.listdir(cdir))
    cdone = 0
    for p in probs:
        total += 1
        m = f'{cdir}/{p}/metrics.json'
        if not os.path.isfile(m): continue
        done += 1; cdone += 1
        try: mm = json.load(open(m))
        except Exception: continue
        # RESULT line from the agent's final text, if present
        # (claude runs: claude-output.json; codex runs: codex-last.txt)
        res, txt = '', ''
        co = f'{cdir}/{p}/claude-output.json'
        cl = f'{cdir}/{p}/codex-last.txt'
        ol = f'{cdir}/{p}/opencode-last.txt'
        if os.path.isfile(co):
            try: txt = json.load(open(co)).get('result') or ''
            except Exception: pass
        elif os.path.isfile(cl):
            try: txt = open(cl).read()
            except Exception: pass
        elif os.path.isfile(ol):
            try: txt = open(ol).read()
            except Exception: pass
        for ln in reversed(txt.strip().splitlines()):
            if ln.startswith('RESULT:'):
                res = ln.split('—')[0].replace('RESULT:','').strip(' -—'); break
        peak = mm.get('mem_peak_bytes')
        peak = f'{peak/2**30:.1f}G' if isinstance(peak, int) else '?'
        rows.append((mm.get('end_epoch', 0), cfg, p, mm.get('exit_code'),
                     mm.get('duration_s'), peak, mm.get('timed_out'), res))
    print(f'  {cfg}: {cdone}/{len(probs)}')
print(f'TOTAL: {done}/{total} done')
if rows:
    print('\nlatest completions:')
    for e, cfg, p, rc, dur, peak, to, res in sorted(rows)[-12:]:
        ts = time.strftime('%H:%M', time.localtime(e)) if e else '?'
        flag = ' TIMEOUT' if to else ''
        print(f'  [{ts}] {cfg.replace("claude-code-","")}/{p}: exit={rc} {dur}s peak={peak}{flag} {res}')
PY
