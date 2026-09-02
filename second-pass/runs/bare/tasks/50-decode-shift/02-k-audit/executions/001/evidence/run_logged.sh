#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
evidence_dir=$(cd "$(dirname "$0")" && pwd)
log_path="$evidence_dir/$log_name"

{
  printf 'PWD: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$log_path"

set +e
"$@" > >(tee -a "$log_path") 2> >(tee -a "$log_path" >&2)
status=$?
set -e

{
  printf '\nEXIT_STATUS: %s\n' "$status"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} | tee -a "$log_path"

exit "$status"
