#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LOG_NAME COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_name="$1"
shift
log_path="/audit-output/evidence/${log_name}"

set +e
{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  "$@"
  command_status="$?"
  printf 'EXIT_STATUS: %s\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$log_path"
pipeline_status="${PIPESTATUS[0]}"
exit "$pipeline_status"
