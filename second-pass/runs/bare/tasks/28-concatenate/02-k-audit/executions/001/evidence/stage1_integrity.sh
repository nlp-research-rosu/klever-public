#!/usr/bin/env bash
set -euxo pipefail

test ! -e /reference/reference-semantics
test ! -L /reference/reference-semantics

test -f /candidate/run-input.json
test ! -L /candidate/run-input.json
test -f /candidate/metrics.json
test ! -L /candidate/metrics.json
test -f /candidate/codex-last.txt
test ! -L /candidate/codex-last.txt
test -f /candidate/codex-output.log
test ! -L /candidate/codex-output.log
test -d /candidate/codex-trace
test ! -L /candidate/codex-trace
test -f /candidate/prompt.py
test ! -L /candidate/prompt.py
test -f /candidate/py2mpy.py
test ! -L /candidate/py2mpy.py
test -f /candidate/solution.py
test ! -L /candidate/solution.py
test -f /candidate/solution.mpy
test ! -L /candidate/solution.mpy
test -f /candidate/semantic.k
test ! -L /candidate/semantic.k
test -f /candidate/verification.k
test ! -L /candidate/verification.k
test -f /candidate/spec.k
test ! -L /candidate/spec.k
test -f /candidate/prove.sh
test ! -L /candidate/prove.sh

cmp /candidate/prompt.py /reference/prompt.py
cmp /candidate/py2mpy.py /reference/py2mpy.py

find /candidate -type l -printf 'SYMLINK %p -> %l\n'
find /candidate -maxdepth 8 -printf '%y %p %s bytes\n' | sort
sha256sum \
  /reference/prompt.py \
  /reference/canonical.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-27-52-019f8927-2991-7be0-81f8-c4c24065748a.jsonl

python3 -m json.tool /candidate/run-input.json
python3 -m json.tool /candidate/metrics.json
sed -n '1,120p' /candidate/codex-last.txt
wc -l -c \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-27-52-019f8927-2991-7be0-81f8-c4c24065748a.jsonl
sed -n '1,50p' /candidate/codex-output.log
tail -50 /candidate/codex-output.log
rg -n '#Top|WarnStuck|kprove|kompile|krun|RESULT:' /candidate/codex-output.log | tail -180
python3 /audit-output/evidence/trace_summary.py \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-27-52-019f8927-2991-7be0-81f8-c4c24065748a.jsonl
