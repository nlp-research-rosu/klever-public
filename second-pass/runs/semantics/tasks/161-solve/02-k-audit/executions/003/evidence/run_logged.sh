#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  printf 'usage: %s LOG_NAME COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}.log"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_path"

"$@" >> "$log_path" 2>&1
command_status=$?
printf '\nEXIT_STATUS: %d\n' "$command_status" >> "$log_path"
sed -n '1,260p' "$log_path"
exit "$command_status"
