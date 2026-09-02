#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  printf 'usage: %s LOG_NAME COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}.log"

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_path"

set +e
"$@" > >(tee -a "$log_path") 2> >(tee -a "$log_path" >&2)
status=$?
set -e

printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log_path"
exit "$status"
