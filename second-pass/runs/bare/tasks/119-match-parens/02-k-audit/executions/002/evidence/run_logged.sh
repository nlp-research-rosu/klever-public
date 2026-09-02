#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

printf 'COMMAND:' | tee "$log_path"
printf ' %q' "$@" | tee -a "$log_path"
printf '\n' | tee -a "$log_path"

"$@" > >(tee -a "$log_path") 2>&1
command_status=$?

printf 'EXIT_STATUS: %d\n' "$command_status" | tee -a "$log_path"
exit "$command_status"
