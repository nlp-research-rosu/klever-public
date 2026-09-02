#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1
  command_status=$?
  printf '\nEXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
} | tee "$log_path"

exit "${PIPESTATUS[0]}"
