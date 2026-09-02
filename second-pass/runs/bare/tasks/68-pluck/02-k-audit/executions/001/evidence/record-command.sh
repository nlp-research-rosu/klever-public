#!/usr/bin/env bash
set -u

audit_log=$1
shift

{
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  audit_status=$?
  printf '[exit status: %d]\n' "$audit_status"
} 2>&1 | tee "$audit_log"

exit "${PIPESTATUS[0]}"
