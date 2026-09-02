#!/usr/bin/env bash
set -u

if (( $# < 3 )); then
  echo "usage: run_logged.sh LOG TIMEOUT_SECONDS COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
timeout_seconds=$2
shift 2
max_lines=${AUDIT_LOG_MAX_LINES:-500}
raw_log=$(mktemp /tmp/audit-log.XXXXXX)

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\nTIMEOUT_SECONDS: %s\n' "$timeout_seconds"
} > "$log_path"

set +e
timeout --signal=TERM --kill-after=10s "$timeout_seconds" "$@" > "$raw_log" 2>&1
command_status=$?
set -e

line_count=$(wc -l < "$raw_log")
{
  printf 'EXIT_STATUS: %s\n' "$command_status"
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  if (( line_count <= max_lines )); then
    cat "$raw_log"
  else
    head -n $((max_lines / 2)) "$raw_log"
    printf '\n[... %s lines omitted by audit logger ...]\n\n' "$((line_count - max_lines))"
    tail -n $((max_lines / 2)) "$raw_log"
  fi
} >> "$log_path"

rm -f "$raw_log"
exit "$command_status"
