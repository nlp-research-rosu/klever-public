#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LABEL COMMAND [ARG ...]" >&2
  exit 2
fi

label=$1
shift
log_dir=$(cd "$(dirname "$0")" && pwd)
log_path="${log_dir}/${label}.log"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '\nEXIT_STATUS: %d\n' "$status"
} >"$log_path" 2>&1

exit "$status"
