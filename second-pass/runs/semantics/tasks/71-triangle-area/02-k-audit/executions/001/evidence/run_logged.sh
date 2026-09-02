#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  printf 'usage: %s LABEL COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

label=$1
shift
log_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
log_file="$log_dir/$label.log"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'START_UTC: %(%Y-%m-%dT%H:%M:%SZ)T\n' -1
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  printf 'END_UTC: %(%Y-%m-%dT%H:%M:%SZ)T\n' -1
  exit "$status"
} >"$log_file" 2>&1
