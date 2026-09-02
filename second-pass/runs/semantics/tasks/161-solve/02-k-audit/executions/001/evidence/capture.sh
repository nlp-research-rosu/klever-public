#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: capture.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$audit_log"

"$@" >>"$audit_log" 2>&1
audit_status=$?

printf 'EXIT_STATUS: %d\n' "$audit_status" >>"$audit_log"
sed -n '1,260p' "$audit_log"
exit "$audit_status"
