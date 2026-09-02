#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$audit_log"

"$@" > >(tee -a "$audit_log") 2> >(tee -a "$audit_log" >&2)
audit_status=$?

printf '\nEXIT_STATUS: %d\n' "$audit_status" | tee -a "$audit_log"
exit "$audit_status"
