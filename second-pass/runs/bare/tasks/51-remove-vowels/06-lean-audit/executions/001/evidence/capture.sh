#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  printf 'usage: %s OUTPUT COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

output=$1
shift

set +e
{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n\n'
  "$@"
  status=$?
  printf '\nEXIT_CODE: %d\n' "$status"
  exit "$status"
} 2>&1 | tee "$output"
status=${PIPESTATUS[0]}
exit "$status"
