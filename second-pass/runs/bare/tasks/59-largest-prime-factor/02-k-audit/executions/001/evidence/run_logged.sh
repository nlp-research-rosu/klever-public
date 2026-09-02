#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log_path="$1"
shift

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf '%s\n' '--- OUTPUT BEGIN ---'
} >"$log_path"

"$@" >>"$log_path" 2>&1
status=$?

{
  printf '%s\n' '--- OUTPUT END ---'
  printf 'EXIT STATUS: %d\n' "$status"
} >>"$log_path"

exit "$status"
