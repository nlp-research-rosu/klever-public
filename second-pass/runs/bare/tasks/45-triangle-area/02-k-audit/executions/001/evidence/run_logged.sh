#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  printf 'usage: %s LOG_PATH COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_path"

set +e
"$@" >> "$log_path" 2>&1
command_status=$?
set -e

printf 'EXIT_STATUS: %d\n' "$command_status" >> "$log_path"
cat "$log_path"
exit "$command_status"
