#!/usr/bin/env bash
set +e
if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi
log=$1
shift
{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '--- OUTPUT BEGIN ---'
} > "$log"
"$@" >> "$log" 2>&1
status=$?
{
  printf '%s\n' '--- OUTPUT END ---'
  printf 'EXIT_STATUS: %d\n' "$status"
} >> "$log"
cat "$log"
exit "$status"
