#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-18-30-019f891e-92d4-7492-943c-e81f33ab55ec.jsonl

run test ! -e /reference/reference-semantics
run find /reference -maxdepth 2 -printf '%y %p -> %l\n'
run find /candidate -maxdepth 1 -printf '%y %f -> %l\n'
run stat -c '%F %a %s %n' \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  "$trace" \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k \
  /candidate/codex-last.txt
run sed -n 1,240p /candidate/codex-last.txt
run python3 /audit-output/evidence/trace_summary.py \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-output.log \
  "$trace"
