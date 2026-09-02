#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  printf 'usage: %s LOG_FILE COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_file=$1
shift
buffer_file="/tmp/audit-work/run-logged-buffer.$$"

cleanup() {
  rm -f "$buffer_file"
}
trap cleanup EXIT HUP INT TERM

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_file"

"$@" > "$buffer_file" 2>&1
command_status=$?
line_count=$(wc -l < "$buffer_file")
byte_count=$(wc -c < "$buffer_file")

{
  printf 'EXIT_STATUS: %s\n' "$command_status"
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  printf 'OUTPUT_BYTES: %s\n' "$byte_count"
  printf '%s\n' '--- OUTPUT (bounded) ---'
  if [ "$line_count" -le 320 ]; then
    sed -n '1,320p' "$buffer_file"
  else
    sed -n '1,220p' "$buffer_file"
    printf '%s\n' "--- OMITTED $((line_count - 300)) MIDDLE LINES ---"
    tail -n 80 "$buffer_file"
  fi
} >> "$log_file"

sed -n '1,220p' "$log_file"
exit "$command_status"
