#!/usr/bin/env bash
set -u

if (( $# < 3 )); then
  printf 'usage: %s LOG_PATH MAX_LINES COMMAND [ARG ...]\n' "$0" >&2
  exit 2
fi

log_path=$1
max_lines=$2
shift 2

tmp_output=$(mktemp /tmp/audit-command-output.XXXXXX)
cleanup() {
  rm -f -- "$tmp_output"
}
trap cleanup EXIT

set +e
"$@" >"$tmp_output" 2>&1
command_status=$?
set -e

line_count=$(wc -l <"$tmp_output")
{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'EXIT_STATUS: %d\n' "$command_status"
  printf 'OUTPUT_LINES: %d\n' "$line_count"
  printf '%s\n' '--- OUTPUT BEGIN ---'
  if (( line_count <= max_lines )); then
    sed -n '1,$p' "$tmp_output"
  else
    head_lines=$((max_lines / 2))
    tail_lines=$((max_lines - head_lines))
    sed -n "1,${head_lines}p" "$tmp_output"
    printf '%s\n' "--- OUTPUT TRUNCATED: omitted $((line_count - max_lines)) middle lines ---"
    tail -n "$tail_lines" "$tmp_output"
  fi
  printf '%s\n' '--- OUTPUT END ---'
} >"$log_path"

sed -n '1,$p' "$log_path"
exit "$command_status"
