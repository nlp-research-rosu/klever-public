#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status"
  return 0
}

run sed -n 1,220p /candidate/run-input.json
run sed -n 1,220p /candidate/metrics.json
run sed -n 1,220p /candidate/codex-last.txt
run sed -n 1,90p /candidate/codex-output.log
run tail -n 140 /candidate/codex-output.log
run rg -n \
  '^RESULT:|^#Top$|WarnStuckClaimState|^\\[Error\\]' \
  /candidate/codex-output.log
run sha256sum \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-18-41-019f898c-9b29-77b2-9431-b031fa9ae74a.jsonl
run sha256sum \
  /candidate/solution.py \
  /tmp/audit-work/99-closest-integer/source/solution.py \
  /candidate/solution.mpy \
  /tmp/audit-work/99-closest-integer/source/solution.mpy \
  /candidate/semantic.k \
  /tmp/audit-work/99-closest-integer/source/semantic.k \
  /candidate/verification.k \
  /tmp/audit-work/99-closest-integer/source/verification.k \
  /candidate/spec.k \
  /tmp/audit-work/99-closest-integer/source/spec.k
