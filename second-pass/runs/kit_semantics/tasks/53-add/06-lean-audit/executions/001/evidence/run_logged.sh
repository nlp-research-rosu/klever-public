#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %q\n' "$PWD"
  printf '%s\n' '--- OUTPUT BEGIN ---'
  "$@"
  rc=$?
  printf '%s\n' '--- OUTPUT END ---'
  printf 'EXIT: %d\n' "$rc"
} >"$log" 2>&1

exit "$rc"
