#!/usr/bin/env bash
set -o pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run-command.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

logfile=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf '\nEXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$logfile"

exit "${PIPESTATUS[0]}"
