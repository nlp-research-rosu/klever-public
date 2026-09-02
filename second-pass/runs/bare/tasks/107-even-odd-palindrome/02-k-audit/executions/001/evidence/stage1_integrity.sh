#!/usr/bin/env bash
set -e
set -u
set -o pipefail
PS4='+ ${BASH_SOURCE}:${LINENO}: '
set -x

test ! -e /reference/reference-semantics
test ! -L /reference/reference-semantics

find /candidate -type l -printf 'SYMLINK %p -> %l\n'
find /candidate -mindepth 1 -maxdepth 1 -printf '%y %m %f\n' | sort

for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy semantic.k verification.k \
  spec.k prove.sh
do
  test -f "/candidate/$artifact"
  test ! -L "/candidate/$artifact"
  stat -c '%F %a %s %n' "/candidate/$artifact"
done

test -d /candidate/codex-trace
test ! -L /candidate/codex-trace
find /candidate/codex-trace -type f -name '*.jsonl' -print

sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /candidate/run-input.json /candidate/metrics.json \
  /candidate/codex-last.txt /candidate/codex-output.log

cmp /reference/prompt.py /candidate/prompt.py
cmp /reference/py2mpy.py /candidate/py2mpy.py

python3 -m json.tool /candidate/run-input.json >/dev/null
python3 -m json.tool /candidate/metrics.json >/dev/null
sed -n '1,120p' /candidate/codex-last.txt

trace_path=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-31-35-019f8998-6dbc-7a80-84ac-a9d9f8fe86d5.jsonl
python3 /audit-output/evidence/trace_inspect.py

wc -cl /candidate/codex-output.log "$trace_path"
sed -n '1,80p' /candidate/codex-output.log
rg -n -i 'kprove|#Top|krun|kompile|error|warning|result:' \
  /candidate/codex-output.log | tail -n 160
tail -n 80 /candidate/codex-output.log
