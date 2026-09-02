#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT STATUS: %d\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee -a "$log_file"

exit "${PIPESTATUS[0]}"
