#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: logged_run.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

logfile=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'START_UTC: %(%Y-%m-%dT%H:%M:%SZ)T\n' -1
} > "$logfile"

set +e
"$@" > >(tee -a "$logfile") 2>&1
status=$?
set -e

{
  printf 'EXIT_STATUS: %d\n' "$status"
  printf 'END_UTC: %(%Y-%m-%dT%H:%M:%SZ)T\n' -1
} | tee -a "$logfile"

exit "$status"
