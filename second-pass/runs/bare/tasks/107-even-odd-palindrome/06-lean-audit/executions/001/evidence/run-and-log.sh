#!/usr/bin/env bash
set -o pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: run-and-log.sh OUTPUT COMMAND [ARG ...]" >&2
  exit 64
fi

output=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n\n'
  "$@"
  status=$?
  printf '\nEXIT_CODE: %s\n' "$status"
  exit "$status"
} 2>&1 | tee "$output"
