#!/usr/bin/env bash
set -u

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
  printf 'WORKDIR: %s\n' "$PWD"
} | tee "$log"

"$@" 2>&1 | tee -a "$log"
command_status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %s\n' "$command_status" | tee -a "$log"
exit "$command_status"
