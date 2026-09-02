#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  echo "usage: record-command.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$audit_log"

set +e
"$@" 2>&1 | tee -a "$audit_log"
audit_status=${PIPESTATUS[0]}
set -e

printf 'EXIT_STATUS: %d\n' "$audit_status" | tee -a "$audit_log"
exit "$audit_status"
