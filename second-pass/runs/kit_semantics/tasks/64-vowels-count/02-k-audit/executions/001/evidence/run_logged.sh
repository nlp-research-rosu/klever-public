#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log_path=$1
shift

rendered_command=
printf -v rendered_command '%q ' "$@"

set +e
{
  printf 'COMMAND: %s\n' "$rendered_command"
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  "$@"
  command_status=$?
  printf 'EXIT_STATUS: %s\n' "$command_status"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  exit "$command_status"
} 2>&1 | tee "$log_path"
pipeline_status=${PIPESTATUS[0]}
exit "$pipeline_status"
