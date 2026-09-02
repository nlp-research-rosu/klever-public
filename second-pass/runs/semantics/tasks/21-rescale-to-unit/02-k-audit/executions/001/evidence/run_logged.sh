#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift
tmp_path=$(mktemp /tmp/audit-work/audit-command.XXXXXX)

printf 'COMMAND: ' > "$log_path"
printf '%q ' "$@" >> "$log_path"
printf '\n' >> "$log_path"

"$@" > "$tmp_path" 2>&1
command_status=$?

printf 'EXIT_STATUS: %d\n' "$command_status" >> "$log_path"
printf '%s\n' 'OUTPUT_BEGIN' >> "$log_path"
sed -n '1,400p' "$tmp_path" >> "$log_path"
output_lines=$(wc -l < "$tmp_path")
if (( output_lines > 400 )); then
  printf '[bounded: first 400 of %d lines]\n' "$output_lines" >> "$log_path"
fi
printf '%s\n' 'OUTPUT_END' >> "$log_path"

sed -n '1,430p' "$log_path"
rm -f -- "$tmp_path"
exit "$command_status"
