#!/usr/bin/env bash
set -uo pipefail

if (( $# < 3 )); then
  echo "usage: run_logged.sh LOG WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
command_workdir=$2
shift 2

{
  printf 'WORKDIR: %s\n' "$command_workdir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf '%s\n' '--- output ---'
  (
    cd "$command_workdir" || exit 125
    "$@"
  )
  status=$?
  printf '%s\n' '--- status ---'
  printf 'EXIT_STATUS: %d\n' "$status"
} >"$log" 2>&1

exit "$status"
