#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'cwd: %s\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
  printf 'started_utc: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '%s\n' '--- output ---'
} > "$log_path"

set +e
"$@" >> "$log_path" 2>&1
status=$?
set -e

{
  printf '%s\n' '--- end output ---'
  printf 'exit_status: %d\n' "$status"
  printf 'finished_utc: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$log_path"

exit "$status"
