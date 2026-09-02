#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  exit "$status"
} 2>&1 | tee "$log"

exit "${PIPESTATUS[0]}"
