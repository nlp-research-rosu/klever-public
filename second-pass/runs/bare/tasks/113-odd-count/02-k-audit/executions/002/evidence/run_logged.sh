#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: run_logged.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

{
  echo "PWD: $(pwd)"
  printf 'COMMAND:'
  printf ' %q' "$@"
  echo
  echo "BEGIN OUTPUT"
} > "$log_file"

"$@" >> "$log_file" 2>&1
command_status=$?

{
  echo "END OUTPUT"
  echo "EXIT STATUS: $command_status"
} >> "$log_file"

exit "$command_status"
