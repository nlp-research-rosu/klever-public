#!/usr/bin/env bash
set -u

if [[ $# -lt 1 ]]; then
  echo "usage: run_logged.sh COMMAND [ARG ...]" >&2
  exit 2
fi

printf 'COMMAND:'
printf ' %q' "$@"
printf '\n'
"$@"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
exit "$status"
