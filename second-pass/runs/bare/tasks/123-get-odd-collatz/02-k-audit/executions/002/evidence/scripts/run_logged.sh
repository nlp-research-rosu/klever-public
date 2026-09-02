#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 3 ]]; then
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
} > "$log"

set +e
(
  cd "$workdir" || exit 125
  "$@"
) >> "$log" 2>&1
status=$?
set -e

printf 'EXIT_STATUS: %s\n' "$status" >> "$log"
exit "$status"
