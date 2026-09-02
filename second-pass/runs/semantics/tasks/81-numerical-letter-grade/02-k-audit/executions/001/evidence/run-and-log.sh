#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG_FILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'START_UTC: '
  date -u +'%Y-%m-%dT%H:%M:%SZ'
} >"$log_file"

"$@" >>"$log_file" 2>&1
command_status=$?

{
  printf 'EXIT_STATUS: %d\n' "$command_status"
  printf 'END_UTC: '
  date -u +'%Y-%m-%dT%H:%M:%SZ'
} >>"$log_file"

exit "$command_status"
