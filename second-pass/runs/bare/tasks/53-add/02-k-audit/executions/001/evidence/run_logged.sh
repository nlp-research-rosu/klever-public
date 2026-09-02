#!/usr/bin/env bash
set -uo pipefail

if (( $# < 3 )) || [[ $2 != "--" ]]; then
  echo "usage: run_logged.sh LOG -- COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift 2

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'BEGIN_OUTPUT\n'
} > "$log"

"$@" 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}

{
  printf 'END_OUTPUT\n'
  printf 'EXIT_STATUS: %d\n' "$status"
} >> "$log"

exit "$status"
