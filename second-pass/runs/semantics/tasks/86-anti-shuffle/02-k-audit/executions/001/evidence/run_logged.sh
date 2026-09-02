#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LOG_NAME COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_name="$1"
shift
log_path="/audit-output/evidence/${log_name}"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_path"

set +e
"$@" >> "$log_path" 2>&1
status=$?
set -e

printf '\nEXIT_STATUS: %d\n' "$status" >> "$log_path"
cat "$log_path"
exit "$status"
