#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LABEL COMMAND..." >&2
  exit 64
fi

label=$1
shift
log="/audit-output/evidence/${label}.log"

{
  echo "WORKDIR: $(pwd)"
  printf 'COMMAND:'
  printf ' %q' "$@"
  echo
  echo "----- OUTPUT -----"
} > "$log"

"$@" >> "$log" 2>&1
status=$?

{
  echo "----- END OUTPUT -----"
  echo "EXIT_STATUS: $status"
} >> "$log"

cat "$log"
exit "$status"
