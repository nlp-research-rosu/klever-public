#!/usr/bin/env bash
set -u
set -o pipefail

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path="$1"
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
} > "$log_path"

"$@" 2>&1 | tee -a "$log_path"
command_status="${PIPESTATUS[0]}"
printf 'EXIT_STATUS: %s\n' "$command_status" | tee -a "$log_path"
exit "$command_status"
