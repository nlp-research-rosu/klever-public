#!/usr/bin/env bash

# Reviewer-authored command recorder. Invoke as:
#   run_logged.sh LOGFILE COMMAND [ARG ...]

set -u

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  "$@"
  command_status=$?
  printf 'EXIT_STATUS: %d\n' "$command_status"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  exit "$command_status"
} >"$log_file" 2>&1
