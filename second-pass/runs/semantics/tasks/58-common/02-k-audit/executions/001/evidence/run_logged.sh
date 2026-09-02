#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  audit_status=$?
  printf '[exit-status] %d\n' "$audit_status"
  exit "$audit_status"
} 2>&1 | tee "$audit_log"

exit "${PIPESTATUS[0]}"
