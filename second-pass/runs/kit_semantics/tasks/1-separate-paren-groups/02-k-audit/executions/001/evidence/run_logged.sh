#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
shift
log_path="/audit-output/evidence/${label}.log"

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
