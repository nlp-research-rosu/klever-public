#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_path"

"$@" >>"$log_path" 2>&1
status=$?

printf 'EXIT_STATUS: %d\n' "$status" >>"$log_path"
exit "$status"
