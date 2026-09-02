#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: record-command.sh OUTPUT COMMAND [ARG ...]" >&2
  exit 2
fi

output=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$output"

set +e
"$@" 2>&1 | tee -a "$output"
status=${PIPESTATUS[0]}
set -e

printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$output"
exit "$status"
