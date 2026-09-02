#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LOG_NAME COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_name="$1"
shift
log_path="/audit-output/evidence/logs/${log_name}.log"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'OUTPUT:\n'
  "$@" 2>&1
  command_status="$?"
  printf 'EXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
} | tee "$log_path"

exit "${PIPESTATUS[0]}"
