#!/usr/bin/env bash
set +e

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '\nEXIT_STATUS: %d\n' "$status"
  exit "$status"
} >"$log" 2>&1
