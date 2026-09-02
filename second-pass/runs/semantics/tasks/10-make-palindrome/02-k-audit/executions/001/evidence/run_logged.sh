#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$audit_log"

"$@" 2>&1 | tee -a "$audit_log"
audit_status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %d\n' "$audit_status" | tee -a "$audit_log"
exit "$audit_status"
