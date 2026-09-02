#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log="$1"
shift
{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status="$?"
  printf 'EXIT_STATUS: %s\n' "$status"
  exit "$status"
} 2>&1 | tee "$log"
exit "${PIPESTATUS[0]}"
