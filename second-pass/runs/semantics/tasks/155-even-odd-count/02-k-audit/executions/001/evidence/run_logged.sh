#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

: > "$audit_log"
exec > >(tee -a "$audit_log") 2>&1

printf 'COMMAND:'
printf ' %q' "$@"
printf '\n'

set +e
"$@"
audit_status=$?
set -e

printf 'EXIT_STATUS: %d\n' "$audit_status"
exit "$audit_status"
