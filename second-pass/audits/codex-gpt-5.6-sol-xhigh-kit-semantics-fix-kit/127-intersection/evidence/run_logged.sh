#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

{
  printf '$'
  printf ' %q' "$@"
  printf '\n'
} | tee -a "$log"

set +e
"$@" 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}
set -e

printf '[exit status: %d]\n' "$status" | tee -a "$log"
exit "$status"
