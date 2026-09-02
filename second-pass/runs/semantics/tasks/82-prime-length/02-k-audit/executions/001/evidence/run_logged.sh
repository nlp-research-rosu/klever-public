#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
shift
log="/audit-output/evidence/${label}.log"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  exit "$status"
} >"$log" 2>&1
