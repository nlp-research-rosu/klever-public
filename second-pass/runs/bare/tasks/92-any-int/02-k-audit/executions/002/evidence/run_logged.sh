#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_FILE COMMAND [ARG ...]" >&2
  exit 2
fi

log_file="$1"
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '--- OUTPUT ---'
} > "$log_file"

"$@" 2>&1 | tee -a "$log_file"
status=${PIPESTATUS[0]}

{
  printf '%s\n' '--- END OUTPUT ---'
  printf 'EXIT_STATUS: %d\n' "$status"
} >> "$log_file"

exit "$status"
