#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT_STATUS: %s\n' "$command_status"
} >"$log_path" 2>&1

cat "$log_path"
exit "$command_status"
