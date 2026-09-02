#!/usr/bin/env bash
set -u

if (( $# < 3 )); then
  echo "usage: $0 LOG_PATH MAX_LINES COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
max_lines=$2
shift 2

tmp_dir=$(mktemp -d /tmp/audit-log.XXXXXX)
tmp_output="$tmp_dir/output"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_path"

"$@" > "$tmp_output" 2>&1
command_status=$?
line_count=$(wc -l < "$tmp_output")

{
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  printf '%s\n' '--- OUTPUT BEGIN ---'
  if (( line_count <= max_lines )); then
    sed -n '1,$p' "$tmp_output"
  else
    head_count=$((max_lines / 2))
    tail_count=$((max_lines - head_count))
    sed -n "1,${head_count}p" "$tmp_output"
    printf '%s\n' "--- $((line_count - max_lines)) LINES OMITTED ---"
    tail -n "$tail_count" "$tmp_output"
  fi
  printf '%s\n' '--- OUTPUT END ---'
  printf 'EXIT_STATUS: %s\n' "$command_status"
} >> "$log_path"

rm -r "$tmp_dir"
exit "$command_status"
