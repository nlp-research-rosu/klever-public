#!/usr/bin/env bash
# Run one exact shell command and preserve bounded stdout/stderr plus exit status.
set -u

if [[ $# -ne 2 ]]; then
  printf 'usage: %s LOG_FILE COMMAND\n' "$0" >&2
  exit 64
fi

log_file=$1
command_text=$2
max_lines=${AUDIT_MAX_LINES:-1200}
temporary_log=$(mktemp /tmp/audit-command.XXXXXX)

printf 'COMMAND: %s\n' "$command_text" >"$log_file"
set +e
bash -o pipefail -c "$command_text" >"$temporary_log" 2>&1
status=$?
set -e

line_count=$(wc -l <"$temporary_log")
if (( line_count <= max_lines )); then
  sed -n "1,${max_lines}p" "$temporary_log" >>"$log_file"
else
  head_count=$((max_lines / 2))
  tail_count=$((max_lines - head_count))
  sed -n "1,${head_count}p" "$temporary_log" >>"$log_file"
  printf '[... %d lines omitted from bounded log ...]\n' \
    "$((line_count - max_lines))" >>"$log_file"
  tail -n "$tail_count" "$temporary_log" >>"$log_file"
fi
printf 'EXIT_STATUS: %d\n' "$status" >>"$log_file"
rm -f "$temporary_log"
cat "$log_file"
exit "$status"
