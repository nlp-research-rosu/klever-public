#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 2
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '----- OUTPUT BEGIN -----'
} >"$log_path"

"$@" >>"$log_path" 2>&1
command_status=$?

{
  printf '%s\n' '----- OUTPUT END -----'
  printf 'EXIT_STATUS: %d\n' "$command_status"
} >>"$log_path"

exit "$command_status"
