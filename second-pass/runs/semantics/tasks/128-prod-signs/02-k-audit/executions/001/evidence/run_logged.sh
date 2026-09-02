#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >"$log" 2>&1

exit "$status"
