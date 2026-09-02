#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

logfile=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$logfile"

set +e
"$@" 2>&1 | tee -a "$logfile"
status=${PIPESTATUS[0]}
set -e

printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$logfile"
exit "$status"
