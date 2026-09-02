#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_FILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

(
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1
  command_status=$?
  printf '\nEXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
) | tee "$log_file"
exit "${PIPESTATUS[0]}"
