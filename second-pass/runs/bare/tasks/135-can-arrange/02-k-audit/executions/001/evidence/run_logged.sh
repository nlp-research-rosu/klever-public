#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf '%s\n' '--- OUTPUT BEGIN ---'
  "$@"
  status=$?
  printf '%s\n' '--- OUTPUT END ---'
  printf 'EXIT STATUS: %d\n' "$status"
  exit "$status"
} 2>&1 | tee "$log"

exit "${PIPESTATUS[0]}"
