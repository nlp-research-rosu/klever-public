#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf '\nEXIT_CODE: %d\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$log_path"
exit "${PIPESTATUS[0]}"
