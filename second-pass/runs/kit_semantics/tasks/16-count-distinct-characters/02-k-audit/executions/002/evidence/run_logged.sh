#!/usr/bin/env bash
set -o pipefail

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 2
fi

audit_log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  audit_status=$?
  printf 'EXIT_STATUS: %s\n' "$audit_status"
  exit "$audit_status"
} 2>&1 | tee "$audit_log"
exit "${PIPESTATUS[0]}"
