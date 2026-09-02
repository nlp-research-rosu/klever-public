#!/usr/bin/env bash
# Run one command without truncating its exit status, recording a reproducible log.
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG_PATH COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  audit_status=$?
  printf '\nEXIT_STATUS: %d\n' "$audit_status"
  exit "$audit_status"
} >"$audit_log" 2>&1
