#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 64
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
  exit "$audit_status"
} >"$audit_log" 2>&1
