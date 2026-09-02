#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG-FILE COMMAND [ARG ...]" >&2
  exit 2
fi

log_file=$1
shift

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$log_file"

set +e
"$@" 2>&1 | tee -a "$log_file"
command_status=${PIPESTATUS[0]}
set -e

printf 'EXIT_STATUS: %d\n' "$command_status" | tee -a "$log_file"
exit "$command_status"
