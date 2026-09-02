#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
evidence_dir=$(cd "$(dirname "$0")" && pwd)
log_path="${evidence_dir}/${log_name}"

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_path"

"$@" >>"$log_path" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status" >>"$log_path"
cat "$log_path"
exit "$status"
