#!/usr/bin/env bash
set -u

if [ "$#" -lt 3 ]; then
  echo "usage: record_command.sh LOG WORKDIR COMMAND..." >&2
  exit 2
fi

log=$1
run_dir=$2
shift 2

{
  printf 'WORKDIR: %s\n' "$run_dir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  (
    cd "$run_dir"
    "$@"
  )
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  exit "$status"
} 2>&1 | tee "$log"

exit "${PIPESTATUS[0]}"
