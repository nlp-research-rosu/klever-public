#!/usr/bin/env bash
set -uo pipefail

if (( $# < 3 )); then
  echo "usage: run_logged.sh LOG WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
workdir=$2
shift 2

{
  printf 'WORKDIR: %s\n' "$workdir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$log"

set +e
(
  cd "$workdir" || exit 125
  "$@"
) > >(tee -a "$log") 2> >(tee -a "$log" >&2)
status=$?
set -e

{
  printf 'EXIT_STATUS: %d\n' "$status"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$log"

exit "$status"
