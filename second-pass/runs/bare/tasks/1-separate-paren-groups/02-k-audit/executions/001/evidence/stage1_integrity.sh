#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

run find /reference -maxdepth 3 -printf '%y %p -> %l\n'
run find /candidate -maxdepth 6 -printf '%y %p -> %l\n'
run test ! -e /reference/reference-semantics
run test ! -L /reference/reference-semantics
run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh
for artifact in \
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
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T03-47-50-019f8902-81a0-7132-bf36-6f07efd73d96.jsonl
do
  run test -f "$artifact"
  run test ! -L "$artifact"
  run test -s "$artifact"
  run stat -c '%F %a %s %n' "$artifact"
done
run python3 -m json.tool /candidate/run-input.json
run python3 -m json.tool /candidate/metrics.json
run wc -l -c \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T03-47-50-019f8902-81a0-7132-bf36-6f07efd73d96.jsonl
run command -v kompile
run command -v krun
run command -v kprove
run kompile --version
run kprove --version
