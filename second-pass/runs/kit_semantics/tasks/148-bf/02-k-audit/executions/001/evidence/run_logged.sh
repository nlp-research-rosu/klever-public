#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_path="$(dirname "$0")/${log_name}.log"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$log_path"

set +e
"$@" 2>&1 | tee -a "$log_path"
status=${PIPESTATUS[0]}
set -e

{
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'EXIT_STATUS: %d\n' "$status"
} | tee -a "$log_path"

exit "$status"
