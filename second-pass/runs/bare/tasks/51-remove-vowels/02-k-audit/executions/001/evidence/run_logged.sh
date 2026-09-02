#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'WORKING_DIRECTORY: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$audit_log"

"$@" >> "$audit_log" 2>&1
audit_status=$?
printf 'EXIT_STATUS: %d\n' "$audit_status" >> "$audit_log"

cat "$audit_log"
exit "$audit_status"
