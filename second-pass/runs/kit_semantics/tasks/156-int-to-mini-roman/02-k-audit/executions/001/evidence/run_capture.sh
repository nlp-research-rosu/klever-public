#!/usr/bin/env bash
set -o pipefail

if [ "$#" -lt 2 ]; then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 2
fi

audit_log=$1
shift

: > "$audit_log"
printf 'COMMAND:' | tee -a "$audit_log"
printf ' %q' "$@" | tee -a "$audit_log"
printf '\n' | tee -a "$audit_log"

"$@" 2>&1 | tee -a "$audit_log"
audit_rc=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %s\n' "$audit_rc" | tee -a "$audit_log"
exit "$audit_rc"
