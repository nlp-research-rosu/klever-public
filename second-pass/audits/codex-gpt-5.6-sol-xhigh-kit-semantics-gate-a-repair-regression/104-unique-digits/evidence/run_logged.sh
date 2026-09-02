#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  printf 'usage: %s LOGFILE COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_file=$1
shift

exec > >(tee "$log_file") 2>&1
printf 'COMMAND:'
printf ' %q' "$@"
printf '\n'
printf 'WORKDIR: %s\n' "$PWD"
printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

"$@"
command_status=$?

printf 'EXIT_STATUS: %d\n' "$command_status"
printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
exit "$command_status"
