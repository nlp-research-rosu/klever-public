#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
shift
log_path="/audit-output/evidence/${label}.log"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf '%s\n' '--- OUTPUT BEGIN ---'
  "$@"
  command_status=$?
  printf '%s\n' '--- OUTPUT END ---'
  printf 'EXIT_STATUS: %d\n' "$command_status"
} 2>&1 | tee "$log_path"

exit "${PIPESTATUS[0]}"
