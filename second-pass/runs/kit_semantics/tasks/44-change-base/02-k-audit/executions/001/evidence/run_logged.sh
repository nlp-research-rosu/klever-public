#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log_file=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$log_file"

"$@" 2>&1 | tee -a "$log_file"
cmd_status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %d\n' "$cmd_status" | tee -a "$log_file"
exit "$cmd_status"
