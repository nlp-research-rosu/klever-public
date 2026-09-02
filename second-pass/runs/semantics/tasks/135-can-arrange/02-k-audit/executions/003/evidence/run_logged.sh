#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 2
fi

audit_log=$1
shift

{
  printf 'CWD: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  audit_status=$?
  printf 'EXIT_STATUS: %d\n' "$audit_status"
  exit "$audit_status"
} > >(tee "$audit_log") 2>&1
