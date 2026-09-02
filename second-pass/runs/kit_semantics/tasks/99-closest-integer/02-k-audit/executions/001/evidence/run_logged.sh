#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log_name=$1
shift
audit_log_path="/audit-output/evidence/${audit_log_name}"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '--- OUTPUT ---'
} > "$audit_log_path"

"$@" >> "$audit_log_path" 2>&1
audit_command_status=$?

{
  printf '%s\n' '--- END OUTPUT ---'
  printf 'EXIT_STATUS: %d\n' "$audit_command_status"
} >> "$audit_log_path"

cat "$audit_log_path"
exit "$audit_command_status"
