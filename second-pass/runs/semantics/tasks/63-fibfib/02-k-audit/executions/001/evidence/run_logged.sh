#!/usr/bin/env bash
set -o pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %q\n' "$PWD"
} >"$log"

"$@" > >(tee -a "$log") 2> >(tee -a "$log" >&2)
status=$?
printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log"
exit "$status"
