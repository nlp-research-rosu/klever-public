#!/usr/bin/env bash
set +e

if (( $# < 2 )); then
  echo "usage: $0 LOG_PATH COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %q\n' "$PWD"
  printf '%s\n' '--- OUTPUT BEGIN ---'
  "$@"
  audit_status=$?
  printf '%s\n' '--- OUTPUT END ---'
  printf 'EXIT_STATUS: %d\n' "$audit_status"
} >"$audit_log_path" 2>&1

exit "$audit_status"
