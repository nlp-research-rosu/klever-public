#!/usr/bin/env bash
set -u

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
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >"$log_path"

set +e
"$@" > >(tee -a "$log_path") 2> >(tee -a "$log_path" >&2)
status=$?
set -e

{
  printf '\nEXIT_STATUS: %s\n' "$status"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} | tee -a "$log_path"

exit "$status"
