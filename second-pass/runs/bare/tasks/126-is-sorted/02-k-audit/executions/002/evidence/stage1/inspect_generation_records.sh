#!/usr/bin/env bash
set -uo pipefail

echo 'COMMAND: python3 /audit-output/evidence/stage1/inspect_generation_trace.py'
python3 /audit-output/evidence/stage1/inspect_generation_trace.py
trace_status=$?
echo "TRACE_EXIT_STATUS=$trace_status"

echo 'COMMAND: rg -n "kompile|kprove|krun|apply_patch|#Top|WarnStuckClaimState|RESULT:" /generation-evidence/codex-output.log'
rg -n 'kompile|kprove|krun|apply_patch|#Top|WarnStuckClaimState|RESULT:' \
  /generation-evidence/codex-output.log
log_status=$?
echo "LOG_RG_EXIT_STATUS=$log_status"

if [[ "$trace_status" -ne 0 || "$log_status" -gt 1 ]]; then
  exit 1
fi
exit 0
