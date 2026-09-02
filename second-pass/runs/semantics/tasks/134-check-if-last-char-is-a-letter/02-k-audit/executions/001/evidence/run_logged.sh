#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  printf 'usage: %s LOG_FILE COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_file=$1
shift
tmp_output=$(mktemp /tmp/audit-work/run-logged.XXXXXX)

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_file"

set +e
"$@" > "$tmp_output" 2>&1
command_status=$?
set -e

{
  printf 'EXIT_STATUS: %d\n' "$command_status"
  printf '%s\n' 'OUTPUT_BEGIN'
  sed -n '1,320p' "$tmp_output"
  output_lines=$(wc -l < "$tmp_output")
  if (( output_lines > 320 )); then
    printf '[bounded log: %d additional lines omitted]\n' "$((output_lines - 320))"
  fi
  printf '%s\n' 'OUTPUT_END'
} >> "$log_file"

sed -n '1,320p' "$tmp_output"
rm -f "$tmp_output"
exit "$command_status"
