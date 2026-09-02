#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
shift
log="/audit-output/evidence/${label}.log"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '\nEXIT_STATUS: %d\n' "$status"
  exit "$status"
} > >(tee "$log") 2>&1
