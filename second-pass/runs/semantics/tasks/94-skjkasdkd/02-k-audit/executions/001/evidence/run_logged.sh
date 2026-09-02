#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift
tmp_output=$(mktemp /tmp/audit-command-output.XXXXXX)

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_path"

set +e
"$@" > "$tmp_output" 2>&1
command_status=$?
set -e

output_bytes=$(wc -c < "$tmp_output")
{
  printf 'OUTPUT_BYTES: %s\n' "$output_bytes"
  printf '%s\n' '--- OUTPUT BEGIN ---'
  if (( output_bytes <= 200000 )); then
    command cat "$tmp_output"
  else
    command head -c 100000 "$tmp_output"
    printf '\n%s\n' '--- OUTPUT TRUNCATED: middle omitted ---'
    command tail -c 100000 "$tmp_output"
  fi
  printf '\n%s\n' '--- OUTPUT END ---'
  printf 'EXIT_STATUS: %s\n' "$command_status"
} >> "$log_path"

command rm -f "$tmp_output"
command cat "$log_path"
exit "$command_status"
