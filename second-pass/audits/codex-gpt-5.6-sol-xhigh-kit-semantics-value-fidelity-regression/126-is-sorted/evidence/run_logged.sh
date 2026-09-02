#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

exec > >(tee "$log_file") 2>&1

printf 'CWD: %q\n' "$PWD"
printf 'COMMAND:'
printf ' %q' "$@"
printf '\n'
printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

set +e
"$@"
command_status=$?
set -e

printf 'EXIT_STATUS: %d\n' "$command_status"
printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
exit "$command_status"
