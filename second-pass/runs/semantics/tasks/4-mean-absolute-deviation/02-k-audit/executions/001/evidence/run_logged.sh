#!/usr/bin/env bash

set +e

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'cwd: %q\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
} >"$audit_log"

"$@" >>"$audit_log" 2>&1
audit_status=$?

printf '\nexit_status: %d\n' "$audit_status" >>"$audit_log"
exit "$audit_status"
