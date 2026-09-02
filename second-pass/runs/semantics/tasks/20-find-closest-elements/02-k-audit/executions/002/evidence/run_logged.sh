#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOGFILE COMMAND [ARG...]" >&2
  exit 2
fi

logfile=$1
shift

{
  printf 'cwd: %q\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
  printf 'started_utc: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$logfile"

set +e
"$@" > >(tee -a "$logfile") 2> >(tee -a "$logfile" >&2)
status=$?
set -e

{
  printf 'exit_status: %d\n' "$status"
  printf 'finished_utc: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} | tee -a "$logfile"

exit "$status"
