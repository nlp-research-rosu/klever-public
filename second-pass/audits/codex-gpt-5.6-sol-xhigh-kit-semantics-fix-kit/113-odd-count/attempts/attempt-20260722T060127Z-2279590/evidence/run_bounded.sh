#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: run_bounded.sh LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log_path=$1
shift
tmp_output=$(mktemp /tmp/audit-command-output.XXXXXX)

{
  printf 'WORKDIR: %s\n' "$PWD"
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
  printf 'EXIT_STATUS: %d\n' "$command_status"
  printf 'OUTPUT_BYTES: %d\n' "$output_bytes"
  if (( output_bytes <= 200000 )); then
    printf '%s\n' '--- OUTPUT (complete) ---'
    sed -n '1,4000p' "$tmp_output"
  else
    printf '%s\n' '--- OUTPUT (first 1000 lines; bounded) ---'
    sed -n '1,1000p' "$tmp_output"
    printf '%s\n' '--- OUTPUT (last 1000 lines; bounded) ---'
    tail -n 1000 "$tmp_output"
  fi
} >> "$log_path"

rm -f "$tmp_output"
exit "$command_status"
