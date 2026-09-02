#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift
mkdir -p "$(dirname "$log_file")"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'START_UTC: '
  date -u +'%Y-%m-%dT%H:%M:%SZ'
} >"$log_file"

set +e
"$@" >>"$log_file" 2>&1
command_status=$?
set -e

{
  printf '\nEXIT_STATUS: %d\n' "$command_status"
  printf 'END_UTC: '
  date -u +'%Y-%m-%dT%H:%M:%SZ'
} >>"$log_file"

exit "$command_status"
