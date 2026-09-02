#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 2
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}.log"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
} >"$log_path" 2>&1
