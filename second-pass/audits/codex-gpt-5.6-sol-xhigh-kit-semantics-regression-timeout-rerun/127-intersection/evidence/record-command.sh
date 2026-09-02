#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift
tmp_output=$(mktemp /tmp/audit-command-output.XXXXXX)

set +e
"$@" >"$tmp_output" 2>&1
command_status=$?
set -e

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'EXIT_STATUS: %s\n' "$command_status"
  output_lines=$(wc -l <"$tmp_output")
  printf 'OUTPUT_LINES: %s\n' "$output_lines"
  if [ "$output_lines" -le 400 ]; then
    cat "$tmp_output"
  else
    printf '%s\n' '--- FIRST 200 LINES ---'
    head -n 200 "$tmp_output"
    printf '%s\n' '--- LAST 200 LINES ---'
    tail -n 200 "$tmp_output"
  fi
} >"$log_path"

rm -f "$tmp_output"
exit "$command_status"
