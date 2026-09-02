#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

mkdir -p "$(dirname "$log_file")"
{
  printf 'cwd: %q\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_file"

set +e
"$@" > >(tee -a "$log_file") 2> >(tee -a "$log_file" >&2)
status=$?
set -e

printf 'exit_status: %d\n' "$status" | tee -a "$log_file"
exit "$status"
