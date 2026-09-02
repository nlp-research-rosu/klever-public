#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: run_logged.sh LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}.log"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '--- OUTPUT ---'
} > "$log_path"

"$@" >> "$log_path" 2>&1
command_status=$?

{
  printf '%s\n' '--- END OUTPUT ---'
  printf 'EXIT STATUS: %s\n' "$command_status"
} >> "$log_path"

cat "$log_path"
exit "$command_status"
