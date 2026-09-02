#!/usr/bin/env bash
set -o pipefail

output=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '\nEXIT_CODE: %s\n' "$status"
  exit "$status"
} 2>&1 | tee "$output"
exit "${PIPESTATUS[0]}"
