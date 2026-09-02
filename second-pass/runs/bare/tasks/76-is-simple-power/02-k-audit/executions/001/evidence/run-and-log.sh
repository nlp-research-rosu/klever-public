#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_PATH COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift
mkdir -p "$(dirname "$log_path")"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
} >"$log_path"

set +e
"$@" >>"$log_path" 2>&1
command_status=$?
set -e

printf 'EXIT_STATUS: %d\n' "$command_status" >>"$log_path"
cat "$log_path"
exit "$command_status"
