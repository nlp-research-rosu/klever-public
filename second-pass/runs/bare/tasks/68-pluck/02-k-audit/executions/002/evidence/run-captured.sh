#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

set +e
{
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf '[exit_status=%d]\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$log_path"
pipeline_status=${PIPESTATUS[0]}
exit "$pipeline_status"
