#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND..." >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT_STATUS: %d\n' "$command_status"
} >"$log_path" 2>&1

exit "$command_status"
