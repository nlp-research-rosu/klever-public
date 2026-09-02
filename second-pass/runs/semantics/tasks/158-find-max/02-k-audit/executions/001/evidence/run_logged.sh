#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_path=$1
shift

exec > >(tee "$log_path") 2>&1

printf 'COMMAND:'
printf ' %q' "$@"
printf '\n'

"$@"
status=$?

printf 'EXIT_STATUS: %d\n' "$status"
exit "$status"
