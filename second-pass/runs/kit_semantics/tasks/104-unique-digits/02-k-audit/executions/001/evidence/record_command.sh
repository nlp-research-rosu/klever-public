#!/usr/bin/env bash
# Execute one command, preserving its exact argv, cwd, combined output, and status.
set -uo pipefail

if [[ "$#" -lt 3 ]]; then
  echo "usage: record_command.sh LOG WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
command_workdir=$2
shift 2

{
  printf 'WORKDIR: %q\n' "$command_workdir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  (
    cd "$command_workdir" || exit 125
    "$@"
  )
  command_status=$?
  printf 'EXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$log_path"
exit "${PIPESTATUS[0]}"
