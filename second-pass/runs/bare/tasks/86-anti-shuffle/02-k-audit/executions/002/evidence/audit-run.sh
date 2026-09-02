#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: audit-run.sh LOG_NAME COMMAND [ARG ...]" >&2
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
  printf '%s\n' '--- OUTPUT ---'
} >"$log_path"

"$@" >>"$log_path" 2>&1
status=$?

{
  printf '%s\n' '--- END OUTPUT ---'
  printf 'EXIT_STATUS: %d\n' "$status"
} >>"$log_path"

cat "$log_path"
exit "$status"
