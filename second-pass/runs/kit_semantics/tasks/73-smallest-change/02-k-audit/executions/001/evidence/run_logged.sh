#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$log_path"

set +e
"$@" 2>&1 | tee -a "$log_path"
command_status=${PIPESTATUS[0]}
set -e

printf 'EXIT_STATUS: %s\n' "$command_status" | tee -a "$log_path"
exit "$command_status"
