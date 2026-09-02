#!/usr/bin/env bash
set -uo pipefail

if (($# < 2)); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\nCWD: %q\n' "$PWD"
} | tee "$log_path"

set +e
"$@" 2>&1 | tee -a "$log_path"
command_status=${PIPESTATUS[0]}
set -e

printf 'EXIT_STATUS: %d\n' "$command_status" | tee -a "$log_path"
exit "$command_status"
