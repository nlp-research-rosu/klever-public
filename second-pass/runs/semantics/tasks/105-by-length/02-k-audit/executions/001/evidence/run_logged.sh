#!/usr/bin/env bash
set +e

if (( $# < 2 )); then
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
  printf '\nEXIT_STATUS: %d\n' "$audit_status"
} >"$audit_log" 2>&1

exit "$audit_status"
