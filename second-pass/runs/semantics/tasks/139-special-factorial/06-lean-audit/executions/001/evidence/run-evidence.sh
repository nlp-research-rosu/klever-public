#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LOGFILE COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

logfile=$1
shift

{
  printf '$'
  printf ' %q' "$@"
  printf '\n'
} > "$logfile"

set +e
"$@" 2>&1 | tee -a "$logfile"
command_status=${PIPESTATUS[0]}
set -e

printf '[exit code: %d]\n' "$command_status" | tee -a "$logfile"
exit "$command_status"
