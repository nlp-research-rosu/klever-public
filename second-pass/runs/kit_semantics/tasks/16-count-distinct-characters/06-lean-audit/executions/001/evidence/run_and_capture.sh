#!/usr/bin/env bash
set +e

output=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_CODE: %d\n' "$status"
  exit "$status"
} 2>&1 | tee "$output"

exit "${PIPESTATUS[0]}"
