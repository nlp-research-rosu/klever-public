#!/usr/bin/env bash
set -uo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: run_logged.sh LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
shift
log="/audit-output/evidence/${label}.log"

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
} >"$log" 2>&1

exit "$status"
