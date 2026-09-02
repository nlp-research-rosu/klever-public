#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_path=$1
shift

: > "$log_path"
{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee -a "$log_path"

set +e
"$@" 2>&1 | tee -a "$log_path"
command_status=${PIPESTATUS[0]}
set -e

printf 'EXIT_STATUS: %s\n' "$command_status" | tee -a "$log_path"
exit "$command_status"
