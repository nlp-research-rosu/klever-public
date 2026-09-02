#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_file=$1
shift

{
  printf 'cwd: %s\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_file"

set +e
"$@" 2>&1 | tee -a "$log_file"
command_status=${PIPESTATUS[0]}
set -e

printf 'exit_status: %d\n' "$command_status" | tee -a "$log_file"
exit "$command_status"
