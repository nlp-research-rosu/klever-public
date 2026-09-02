#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: run-logged.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log_path=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  audit_command_status=$?
  printf '\nEXIT_STATUS: %d\n' "$audit_command_status"
  exit "$audit_command_status"
} 2>&1 | tee "$audit_log_path"

exit "${PIPESTATUS[0]}"
