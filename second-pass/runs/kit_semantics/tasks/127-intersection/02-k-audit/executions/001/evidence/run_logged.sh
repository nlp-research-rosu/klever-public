#!/usr/bin/env bash
set -u

if (( $# < 3 )); then
  echo "usage: $0 LOG_NAME WORKDIR COMMAND [ARG ...]" >&2
  exit 2
fi

log_name=$1
command_workdir=$2
shift 2
log_path="/audit-output/evidence/${log_name}.log"

{
  printf 'WORKDIR: %s\n' "$command_workdir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_path"

cd "$command_workdir" || exit 125
"$@" >> "$log_path" 2>&1
command_status=$?

printf 'EXIT_STATUS: %d\n' "$command_status" >> "$log_path"
sed -n '1,240p' "$log_path"
exit "$command_status"
