#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}"

: > "${log_path}"
{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} | tee -a "${log_path}"

"$@" 2>&1 | tee -a "${log_path}"
command_status=${PIPESTATUS[0]}

{
  printf 'EXIT_STATUS: %d\n' "${command_status}"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} | tee -a "${log_path}"

exit "${command_status}"
