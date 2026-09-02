#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '--- OUTPUT ---'
} > "$audit_log"

"$@" >> "$audit_log" 2>&1
audit_status=$?

{
  printf '%s\n' '--- END OUTPUT ---'
  printf 'EXIT_STATUS: %d\n' "$audit_status"
} >> "$audit_log"

exit "$audit_status"
