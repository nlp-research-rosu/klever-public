#!/usr/bin/env bash
set -uo pipefail
overall_status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT STATUS: %d\n' "$status"
  if (( status != 0 )); then
    overall_status=1
  fi
  return 0
}

run python3 /audit-output/evidence/stage1_integrity.py
run findmnt -T /candidate -n -o TARGET,OPTIONS
run findmnt -T /generation-evidence -n -o TARGET,OPTIONS
run findmnt -T /audit-input.json -n -o TARGET,OPTIONS
run findmnt -T /audit-campaign-lock.json -n -o TARGET,OPTIONS
run findmnt -T /reference/canonical.py -n -o TARGET,OPTIONS
run findmnt -T /reference/prompt.py -n -o TARGET,OPTIONS
run findmnt -T /reference/py2mpy.py -n -o TARGET,OPTIONS
run kompile --version
run kprove --version
run krun --version

for record in \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json
do
  run python3 -m json.tool "$record"
done

run wc -c -l \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T04-26-36-019f8925-fce7-7f52-b753-b35e7b37f1fe.jsonl

run python3 /audit-output/evidence/stage1_generation_summary.py

exit "$overall_status"
