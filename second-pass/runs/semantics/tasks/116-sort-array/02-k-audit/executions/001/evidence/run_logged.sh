#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  set +e
  "$@"
  command_status=$?
  set -e
  printf 'EXIT_STATUS: %s\n' "$command_status"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  exit "$command_status"
} 2>&1 | tee "$log_path"

exit "${PIPESTATUS[0]}"
