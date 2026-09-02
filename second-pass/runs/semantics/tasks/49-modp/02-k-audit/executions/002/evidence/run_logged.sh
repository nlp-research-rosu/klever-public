#!/usr/bin/env bash
# Run one audit command, recording the exact command, output, and exit status.
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
} > "$audit_log"

"$@" >> "$audit_log" 2>&1
audit_status=$?
printf 'EXIT_STATUS: %d\n' "$audit_status" >> "$audit_log"
exit "$audit_status"
