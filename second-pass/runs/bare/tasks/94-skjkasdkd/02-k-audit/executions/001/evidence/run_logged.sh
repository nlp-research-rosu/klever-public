#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf '%s\n' '--- OUTPUT ---'
} > "$log_file"

"$@" 2>&1 | tee -a "$log_file"
command_status=${PIPESTATUS[0]}

{
  printf '%s\n' '--- END OUTPUT ---'
  printf 'EXIT_STATUS: %d\n' "$command_status"
} >> "$log_file"

exit "$command_status"
