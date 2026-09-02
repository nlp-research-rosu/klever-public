#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift
mkdir -p -- "$(dirname -- "$log_file")"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$log_file"

set +e
"$@" 2>&1 | tee -a "$log_file"
command_status=${PIPESTATUS[0]}
set -e

printf 'EXIT STATUS: %d\n' "$command_status" | tee -a "$log_file"
exit "$command_status"
