#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'cwd: %q\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_path"

set +e
"$@" > >(tee -a "$log_path") 2> >(tee -a "$log_path" >&2)
command_status=$?
set -e

printf 'exit_status: %d\n' "$command_status" | tee -a "$log_path"
exit "$command_status"
