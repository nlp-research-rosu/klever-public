#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: run_logged.sh LOG_PATH COMMAND [ARG ...]" >&2
  exit 2
fi

log_path="$1"
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$log_path"

"$@" 2>&1 | tee -a "$log_path"
status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %s\n' "$status" | tee -a "$log_path"
exit "$status"
