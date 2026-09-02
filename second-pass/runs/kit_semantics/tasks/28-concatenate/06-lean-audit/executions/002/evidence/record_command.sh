#!/usr/bin/env bash
set +e

output=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf '\nEXIT_CODE: %d\n' "$command_status"
} >"$output" 2>&1

exit "$command_status"
