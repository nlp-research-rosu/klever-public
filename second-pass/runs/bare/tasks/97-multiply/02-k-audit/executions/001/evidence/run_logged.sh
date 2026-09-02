#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

audit_label=$1
shift
audit_log="/audit-output/evidence/${audit_label}.log"

{
  printf 'UTC_START: '
  date -u '+%Y-%m-%dT%H:%M:%SZ'
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  audit_status=$?
  printf 'EXIT_STATUS: %d\n' "$audit_status"
  printf 'UTC_END: '
  date -u '+%Y-%m-%dT%H:%M:%SZ'
  exit "$audit_status"
} 2>&1 | tee "$audit_log"

exit "${PIPESTATUS[0]}"
