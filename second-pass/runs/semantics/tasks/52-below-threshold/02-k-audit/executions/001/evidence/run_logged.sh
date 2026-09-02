#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

logfile="$1"
shift
quoted_command="$(printf '%q ' "$@")"
script_command="printf '%s\n' 'COMMAND: $quoted_command'; $quoted_command; status=\$?; printf '%s\n' \"EXIT_STATUS=\$status\"; exit \$status"
script -q -e -c "$script_command" "$logfile"
