#!/usr/bin/env bash
set +e

if [[ $# -lt 2 ]]; then
  echo "usage: capture.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '--- OUTPUT ---'
} > "$log_file"

"$@" >> "$log_file" 2>&1
command_status=$?

{
  printf '%s\n' '--- END OUTPUT ---'
  printf 'EXIT STATUS: %d\n' "$command_status"
} >> "$log_file"

exit "$command_status"
