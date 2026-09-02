#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '--- OUTPUT ---'
} >"$log_path"

"$@" >>"$log_path" 2>&1
command_status=$?

{
  printf '%s\n' '--- END OUTPUT ---'
  printf 'EXIT STATUS: %d\n' "$command_status"
} >>"$log_path"

cat "$log_path"
exit "$command_status"
