#!/usr/bin/env bash
set -o pipefail

if (( $# < 2 )); then
  printf 'usage: %s LOG_NAME COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}.log"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf '\nEXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$log_path"
exit "${PIPESTATUS[0]}"
