#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}"
tmp_path=$(mktemp /tmp/audit-work/command-output.XXXXXX)

started=$(date --iso-8601=seconds)
printf 'started: %s\n' "$started" > "$log_path"
printf 'cwd: %s\n' "$PWD" >> "$log_path"
printf 'command:' >> "$log_path"
printf ' %q' "$@" >> "$log_path"
printf '\n' >> "$log_path"

"$@" > "$tmp_path" 2>&1
status=$?
line_count=$(wc -l < "$tmp_path")
byte_count=$(wc -c < "$tmp_path")

printf 'exit_status: %s\n' "$status" >> "$log_path"
printf 'output_lines: %s\n' "$line_count" >> "$log_path"
printf 'output_bytes: %s\n' "$byte_count" >> "$log_path"
printf '%s\n' '--- bounded output (first 240 lines) ---' >> "$log_path"
sed -n '1,240p' "$tmp_path" >> "$log_path"
if (( line_count > 280 )); then
  printf '%s\n' '--- omitted middle; final 40 lines follow ---' >> "$log_path"
  tail -40 "$tmp_path" >> "$log_path"
fi

rm -f -- "$tmp_path"
exit "$status"
