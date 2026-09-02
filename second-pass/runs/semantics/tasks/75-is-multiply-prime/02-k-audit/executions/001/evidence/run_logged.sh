#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift

if [[ ! "$log_name" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "invalid log name: $log_name" >&2
  exit 64
fi

log_path="/audit-output/evidence/$log_name"

{
  printf 'cwd: %q\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_path"

set +e
"$@" 2>&1 | tee -a "$log_path"
command_status=${PIPESTATUS[0]}
set -e

printf 'exit_status: %d\n' "$command_status" | tee -a "$log_path"
exit "$command_status"
