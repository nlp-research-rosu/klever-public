#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

: > "$audit_log"
{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
} | tee -a "$audit_log"

set +e
"$@" 2>&1 | tee -a "$audit_log"
audit_status=${PIPESTATUS[0]}
set -e

printf 'EXIT_STATUS: %s\n' "$audit_status" | tee -a "$audit_log"
exit "$audit_status"
