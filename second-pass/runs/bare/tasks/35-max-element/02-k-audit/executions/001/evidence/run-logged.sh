#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: run-logged.sh LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
shift
log="/audit-output/evidence/${label}.log"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'START_UTC: %(%Y-%m-%dT%H:%M:%SZ)T\n' -1
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  printf 'END_UTC: %(%Y-%m-%dT%H:%M:%SZ)T\n' -1
  exit "$status"
} >"$log" 2>&1
