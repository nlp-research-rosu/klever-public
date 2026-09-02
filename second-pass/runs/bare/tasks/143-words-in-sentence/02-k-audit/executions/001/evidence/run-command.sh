#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

mkdir -p "$(dirname "$log")"
{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '\nEXIT_STATUS: %d\n' "$status"
} >"$log" 2>&1

exit "$status"
