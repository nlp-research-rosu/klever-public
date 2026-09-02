#!/usr/bin/env bash

# Reviewer-authored command recorder. Each invocation creates one bounded log
# containing the exact argv, combined output, and exit status.
set +e

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$audit_log"

"$@" >> "$audit_log" 2>&1
audit_status=$?

printf '\nEXIT_STATUS: %d\n' "$audit_status" >> "$audit_log"
exit "$audit_status"
