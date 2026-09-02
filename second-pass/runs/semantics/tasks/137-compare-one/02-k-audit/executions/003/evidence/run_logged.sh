#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift
mkdir -p "$(dirname "$log")"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log"

set +e
"$@" > >(tee -a "$log") 2> >(tee -a "$log" >&2)
status=$?
set -e
printf '\nEXIT_STATUS: %d\n' "$status" | tee -a "$log"
exit "$status"
