#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
shift

if [[ ! "$label" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "invalid evidence label: $label" >&2
  exit 64
fi

evidence_dir=$(cd -- "$(dirname -- "$0")" && pwd)
log_path="$evidence_dir/$label.log"

{
  printf 'working-directory: %q\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf '\nexit-status: %d\n' "$command_status"
  exit "$command_status"
} 2>&1 | tee "$log_path"

exit "${PIPESTATUS[0]}"
