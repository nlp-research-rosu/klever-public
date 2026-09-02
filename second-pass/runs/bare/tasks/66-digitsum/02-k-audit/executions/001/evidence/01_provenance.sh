#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run test ! -e /reference/reference-semantics
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py
run stat -c '%F | mode=%a | size=%s | %n' \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/prove.sh
run find /candidate -type l -printf '%p -> %l\n'
run find /candidate -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n'
run sha256sum \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-23-03-019f8959-aee9-7291-b260-1ab7e6efadce.jsonl
run wc -lc \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-23-03-019f8959-aee9-7291-b260-1ab7e6efadce.jsonl
run sed -n '1,80p' /candidate/run-input.json
run sed -n '1,80p' /candidate/metrics.json
run sed -n '1,100p' /candidate/codex-last.txt
run sed -n '1,35p' /candidate/codex-output.log
run tail -40 /candidate/codex-output.log
run bash -lc 'rg -n "#Top|WarnStuckClaimState|RESULT:|kprove|kompile semantic.k" /candidate/codex-output.log | tail -120'
run python3 /audit-output/evidence/trace_summary.py
