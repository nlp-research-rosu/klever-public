#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}"

printf 'WORKDIR: %q\n' "$PWD" | tee "$log_path"
printf 'COMMAND:' | tee -a "$log_path"
printf ' %q' "$@" | tee -a "$log_path"
printf '\n' | tee -a "$log_path"

"$@" 2>&1 | tee -a "$log_path"
command_status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %d\n' "$command_status" | tee -a "$log_path"
exit "$command_status"
