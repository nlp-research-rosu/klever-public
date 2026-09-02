#!/usr/bin/env bash
set -u

if (( $# < 3 )); then
  echo "usage: $0 LOG_BASENAME WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

log_basename=$1
command_workdir=$2
shift 2
log_path="/audit-output/evidence/${log_basename}.log"

{
  printf 'WORKDIR: %q\n' "$command_workdir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf '%s\n' '--- OUTPUT BEGIN ---'
  cd "$command_workdir" || exit 72
  "$@"
  command_status=$?
  printf '%s\n' '--- OUTPUT END ---'
  printf 'EXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
} >"$log_path" 2>&1
