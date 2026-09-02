#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_and_log.sh LABEL COMMAND [ARG ...]" >&2
  exit 2
fi

label=$1
shift
log="/audit-output/evidence/${label}.log"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  exit "$status"
} 2>&1 | tee "$log"
exit "${PIPESTATUS[0]}"
