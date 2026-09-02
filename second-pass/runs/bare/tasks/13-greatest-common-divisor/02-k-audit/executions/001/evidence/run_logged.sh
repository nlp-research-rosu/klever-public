#!/usr/bin/env bash
set -u

if [[ "$#" -lt 3 ]]; then
  echo "usage: run_logged.sh LOG WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
run_dir=$2
shift 2

{
  printf 'WORKDIR: %q\n' "$run_dir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf '%s\n' '--- OUTPUT BEGIN ---'
  (
    cd "$run_dir" || exit 125
    "$@"
  )
  command_status=$?
  printf '%s\n' '--- OUTPUT END ---'
  printf 'EXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$log_path"

exit "${PIPESTATUS[0]}"
