#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LOG_FILE COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_file=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT STATUS: %d\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$log_file"

exit "${PIPESTATUS[0]}"
