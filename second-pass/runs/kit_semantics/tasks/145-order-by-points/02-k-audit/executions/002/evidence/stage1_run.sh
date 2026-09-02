#!/usr/bin/env bash
set -uo pipefail

run_and_record() {
  echo "\$ $*"
  "$@"
  command_status=$?
  echo "EXIT: $command_status"
  return "$command_status"
}

overall=0
run_and_record python3 /audit-output/evidence/stage1_integrity.py || overall=1
run_and_record sha256sum \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T03-21-57-019f985d-e317-7930-a644-ca6d2ae8baab.jsonl \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py || overall=1
run_and_record cmp /reference/prompt.py /candidate/prompt.py || overall=1
run_and_record cmp /reference/py2mpy.py /candidate/py2mpy.py || overall=1
run_and_record diff -r --no-dereference \
  /reference/reference-semantics \
  /candidate/reference-semantics || overall=1
run_and_record find \
  /candidate \
  /reference \
  /generation-evidence \
  -type l -print || overall=1
run_and_record python3 /audit-output/evidence/trace_commands.py || overall=1
echo "STAGE1 SCRIPT EXIT: $overall"
exit "$overall"
