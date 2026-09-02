#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  echo "usage: capture.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  "$@"
  audit_status=$?
  printf 'EXIT_STATUS: %d\n' "$audit_status"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  exit "$audit_status"
} 2>&1 | tee "$audit_log"

exit "${PIPESTATUS[0]}"
