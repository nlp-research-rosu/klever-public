#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}.log"

{
  echo "UTC_START: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "CWD: $(pwd)"
  printf 'COMMAND:'
  printf ' %q' "$@"
  echo
} > "$log_path"

"$@" >> "$log_path" 2>&1
status=$?

{
  echo "EXIT_STATUS: $status"
  echo "UTC_END: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$log_path"

exit "$status"
