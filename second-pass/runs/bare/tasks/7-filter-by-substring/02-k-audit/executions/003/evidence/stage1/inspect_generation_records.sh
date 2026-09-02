#!/usr/bin/env bash
set -u

printf '%s\n' '$ python3 /audit-output/evidence/stage1/inspect_generation_records.py'
python3 /audit-output/evidence/stage1/inspect_generation_records.py
printf 'EXIT: %d\n' "$?"

printf '%s\n' '$ rg -n -C 2 "bash -n prove.sh|./prove.sh|all six|#Top|WarnTrivialClaim|KPROVE_PASSED|RESULT:" /generation-evidence/codex-output.log (bounded tail)'
rg -n -C 2 \
  'bash -n prove\.sh|\./prove\.sh|all six|#Top|WarnTrivialClaim|KPROVE_PASSED|RESULT:' \
  /generation-evidence/codex-output.log \
  | tail -n 260
printf 'EXIT: %d\n' "${PIPESTATUS[0]}"
