#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  run_status=$?
  printf '\nEXIT_STATUS: %d\n' "$run_status"
  exit "$run_status"
} 2>&1 | tee "$log_path"

exit "${PIPESTATUS[0]}"
