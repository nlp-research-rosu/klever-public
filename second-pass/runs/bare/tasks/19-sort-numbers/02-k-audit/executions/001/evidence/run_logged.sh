#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_PATH COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log_path=$1
shift
audit_tmp_log=$(mktemp /tmp/audit-command.XXXXXX)

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
} > "$audit_tmp_log"

set +e
"$@" >> "$audit_tmp_log" 2>&1
audit_command_status=$?
set -e

printf 'EXIT_STATUS: %d\n' "$audit_command_status" >> "$audit_tmp_log"
audit_line_count=$(wc -l < "$audit_tmp_log")

if (( audit_line_count <= 1600 )); then
  cp -- "$audit_tmp_log" "$audit_log_path"
else
  {
    head -n 1200 "$audit_tmp_log"
    printf '\n[... bounded log: %d total lines; middle omitted ...]\n\n' "$audit_line_count"
    tail -n 400 "$audit_tmp_log"
  } > "$audit_log_path"
fi

rm -f -- "$audit_tmp_log"
cat -- "$audit_log_path"
exit "$audit_command_status"
