#!/usr/bin/env bash
set -o pipefail

if [[ $# -lt 2 ]]; then
  printf 'usage: %s LABEL COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

label=$1
shift
log_path="/audit-output/evidence/${label}.log"

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$log_path"

exit "${PIPESTATUS[0]}"
