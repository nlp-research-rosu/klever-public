#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log=$1
shift

exec > >(tee "$log") 2>&1
printf 'WORKDIR: %q\n' "$PWD"
printf 'COMMAND:'
printf ' %q' "$@"
printf '\n'
printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
"$@"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
exit "$status"
