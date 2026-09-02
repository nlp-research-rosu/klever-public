#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'cwd: %s\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
  printf 'started_utc: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  "$@"
  command_status=$?
  printf 'exit_status: %d\n' "$command_status"
  printf 'finished_utc: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  exit "$command_status"
} >"$log_path" 2>&1
