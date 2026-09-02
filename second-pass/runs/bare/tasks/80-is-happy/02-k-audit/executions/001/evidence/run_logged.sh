#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift
tmp_output=$(mktemp /tmp/audit-command-output.XXXXXX)

{
  printf 'WORKDIR: %s\n' "$PWD"
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
  printf '%s\n' '--- OUTPUT BEGIN ---'
  sed -n '1,800p' "$tmp_output"
  output_lines=$(wc -l < "$tmp_output")
  if [ "$output_lines" -gt 800 ]; then
    printf '%s\n' "--- OUTPUT TRUNCATED: ${output_lines} total lines; final 80 follow ---"
    tail -n 80 "$tmp_output"
  fi
  printf '%s\n' '--- OUTPUT END ---'
} >> "$log_file"

cat "$log_file"
unlink "$tmp_output"
exit "$command_status"
