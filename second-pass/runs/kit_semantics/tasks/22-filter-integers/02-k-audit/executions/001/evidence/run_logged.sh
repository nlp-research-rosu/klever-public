#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 2
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}"

{
  printf 'cwd: %q\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
  printf 'started_utc: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$log_path"

"$@" > >(tee -a "$log_path") 2> >(tee -a "$log_path" >&2)
status=$?

{
  printf '\nexit_status: %d\n' "$status"
  printf 'finished_utc: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$log_path"

exit "$status"
