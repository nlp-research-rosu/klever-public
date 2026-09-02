#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: capture.sh LOG COMMAND [ARG ...]" >&2
  exit 2
fi

audit_log=$1
shift

{
  printf '[cwd] %q\n' "$PWD"
  printf '[command]'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  audit_status=$?
  printf '\n[exit_status] %d\n' "$audit_status"
  exit "$audit_status"
} 2>&1 | tee "$audit_log"

exit "${PIPESTATUS[0]}"
