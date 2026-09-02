#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

audit_log="$1"
shift

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$audit_log"

"$@" 2>&1 | tee -a "$audit_log"
audit_status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %d\n' "$audit_status" | tee -a "$audit_log"
exit "$audit_status"
