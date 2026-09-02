#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log_name=$1
shift
audit_log_path="/audit-output/evidence/${audit_log_name}.log"
audit_tmp_log=$(mktemp /tmp/audit-work/audit-command.XXXXXX)

"$@" >"$audit_tmp_log" 2>&1
audit_status=$?
audit_line_count=$(wc -l <"$audit_tmp_log")
audit_byte_count=$(wc -c <"$audit_tmp_log")

{
  printf 'cwd: %q\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
  printf 'captured_lines: %s\n' "$audit_line_count"
  printf 'captured_bytes: %s\n' "$audit_byte_count"
  printf '%s\n' '--- output ---'
  if (( audit_line_count <= 600 )); then
    sed -n '1,600p' "$audit_tmp_log"
  else
    sed -n '1,300p' "$audit_tmp_log"
    printf '%s\n' "--- omitted $((audit_line_count - 600)) middle lines ---"
    tail -n 300 "$audit_tmp_log"
  fi
  printf '%s\n' '--- status ---'
  printf 'exit_status: %s\n' "$audit_status"
} >"$audit_log_path"

rm -f "$audit_tmp_log"
exit "$audit_status"
