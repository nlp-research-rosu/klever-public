#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
evidence_dir=$(cd -- "$(dirname -- "$0")" && pwd)
log_path="$evidence_dir/$log_name"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
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
