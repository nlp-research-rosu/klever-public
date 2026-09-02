#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

audit_log=$1
shift
: > "$audit_log"
{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee -a "$audit_log"

"$@" 2>&1 | tee -a "$audit_log"
audit_status=${PIPESTATUS[0]}
printf 'EXIT_STATUS=%s\n' "$audit_status" | tee -a "$audit_log"
exit "$audit_status"
