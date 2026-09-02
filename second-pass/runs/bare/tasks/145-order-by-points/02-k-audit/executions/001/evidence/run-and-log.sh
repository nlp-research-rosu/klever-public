#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 3 ]]; then
  echo "usage: run-and-log.sh LOG WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
workdir=$2
shift 2

(
  printf 'WORKDIR: %s\n' "$workdir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  cd "$workdir" || exit 125
  "$@"
  command_status=$?
  printf '\nEXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
) 2>&1 | tee "$log"

exit "${PIPESTATUS[0]}"
