#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label="$1"
shift
log="/audit-output/evidence/${label}.log"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$log"

"$@" 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}

printf 'EXIT STATUS: %d\n' "$status" | tee -a "$log"
exit "$status"
