#!/usr/bin/env bash
# Run one command, preserving its exact argv, bounded combined output, and status.
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log_path="$1"
shift
mkdir -p "$(dirname "$log_path")"
{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT_STATUS: %s\n' "$command_status"
  exit "$command_status"
} >"$log_path" 2>&1
