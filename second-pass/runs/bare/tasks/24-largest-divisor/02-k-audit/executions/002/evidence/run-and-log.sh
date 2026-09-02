#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift
mkdir -p "$(dirname "$log")"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '--- OUTPUT ---'
  "$@"
  status=$?
  printf '%s\n' '--- END OUTPUT ---'
  printf 'EXIT_STATUS: %d\n' "$status"
  exit "$status"
} 2>&1 | tee "$log"

exit "${PIPESTATUS[0]}"
