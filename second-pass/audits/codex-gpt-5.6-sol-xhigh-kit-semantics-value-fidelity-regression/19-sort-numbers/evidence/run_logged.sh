#!/usr/bin/env bash
set -uo pipefail

if (( $# < 3 )); then
  echo "usage: $0 LOGFILE TIMEOUT_SECONDS COMMAND [ARG ...]" >&2
  exit 64
fi

logfile=$1
timeout_seconds=$2
shift 2

: > "$logfile"
{
  printf 'cwd: %s\n' "$PWD"
  printf 'utc: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
  printf 'timeout_seconds: %s\n' "$timeout_seconds"
} | tee -a "$logfile"

set +e
timeout --foreground "$timeout_seconds" "$@" 2>&1 | tee -a "$logfile"
command_status=${PIPESTATUS[0]}
set -e

printf 'exit_status: %s\n' "$command_status" | tee -a "$logfile"
exit "$command_status"
