#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 64
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
