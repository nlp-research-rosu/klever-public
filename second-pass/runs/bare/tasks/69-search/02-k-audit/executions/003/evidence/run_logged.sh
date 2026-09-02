#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: run_logged.sh LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label="$1"
shift
log="/audit-output/evidence/logs/${label}.log"

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'START_UTC: '
  date -u '+%Y-%m-%dT%H:%M:%SZ'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  printf 'END_UTC: '
  date -u '+%Y-%m-%dT%H:%M:%SZ'
  exit "$status"
} >"$log" 2>&1
