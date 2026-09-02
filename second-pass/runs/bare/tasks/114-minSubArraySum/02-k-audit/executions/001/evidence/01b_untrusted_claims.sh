#!/usr/bin/env bash
set -u

run() {
  local cmd="$1"
  printf '$ %s\n' "$cmd"
  bash -o pipefail -c "$cmd"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

TRACE=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-42-25-019f89a2-5723-72d1-9231-c4bd7aff3420.jsonl

run "sha256sum /candidate/run-input.json /candidate/metrics.json /candidate/codex-last.txt /candidate/codex-output.log '$TRACE'"
run "python3 -m json.tool /candidate/run-input.json"
run "python3 -m json.tool /candidate/metrics.json"
run "sed -n '1,120p' /candidate/codex-last.txt"
run "sed -n '1,75p' /candidate/codex-output.log"
run "tail -n 90 /candidate/codex-output.log"
run "rg -n -i '#top|warnstuck|error.*prover|completed successfully|result:' /candidate/codex-output.log | tail -n 120"
run "python3 /audit-output/evidence/untrusted_trace_summary.py '$TRACE'"
