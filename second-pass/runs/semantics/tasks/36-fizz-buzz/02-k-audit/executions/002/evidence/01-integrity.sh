#!/usr/bin/env bash
set -uo pipefail

LOG=/audit-output/evidence/01-integrity.log
: > "$LOG"

run() {
  printf '$ %s\n' "$*" >> "$LOG"
  "$@" >> "$LOG" 2>&1
  status=$?
  printf 'EXIT: %s\n\n' "$status" >> "$LOG"
  return 0
}

run python3 /audit-output/evidence/check_integrity.py
run python3 -m json.tool /run.json
run python3 -m json.tool /task.json
run python3 -m json.tool /generation-result.json
run python3 -m json.tool /generation-evidence/invocation.json
run python3 -m json.tool /generation-evidence/metrics.json
run python3 -m json.tool /generation-evidence/usage.json
run python3 -m json.tool /generation-evidence/legacy-metrics.json
run python3 -m json.tool /generation-evidence/legacy-run-input.json
run sed -n 1,220p /generation-evidence/codex-last.txt
run sed -n 1,260p /generation-evidence/prompt.txt
run sed -n 1,100p /generation-evidence/codex-output.log
run tail -120 /generation-evidence/codex-output.log
run rg -n \
  -e KPROVE_PASSED \
  -e '#Top' \
  -e '506-case' \
  -e 'universal digit-loop' \
  /generation-evidence/codex-output.log
run python3 /audit-output/evidence/summarize_trace.py
run sha256sum /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T23-05-54-019f8d26-be15-7193-af5e-cbed9f66562d.jsonl
run wc -l -c /generation-evidence/codex-output.log /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T23-05-54-019f8d26-be15-7193-af5e-cbed9f66562d.jsonl
