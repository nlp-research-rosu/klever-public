#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  printf 'usage: %s LOGFILE COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$audit_log"

set +e
"$@" >> "$audit_log" 2>&1
audit_status=$?
set -e

printf 'EXIT_STATUS: %d\n' "$audit_status" >> "$audit_log"
exit "$audit_status"
