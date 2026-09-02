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
} > "$log"

set +e
"$@" > >(tee -a "$log") 2> >(tee -a "$log" >&2)
status=$?
set -e

printf '\nEXIT_STATUS: %d\n' "$status" | tee -a "$log"
exit "$status"
