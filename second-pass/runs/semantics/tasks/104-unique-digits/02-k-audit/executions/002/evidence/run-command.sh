#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: run-command.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_path"

set +e
"$@" > >(tee -a "$log_path") 2> >(tee -a "$log_path" >&2)
command_status=$?
set -e

printf '\nEXIT STATUS: %d\n' "$command_status" | tee -a "$log_path"
exit "$command_status"
