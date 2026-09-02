#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  printf 'usage: %s LOGFILE COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_file=$1
shift
tmp_file=$(mktemp /tmp/audit-command.XXXXXX)

printf 'WORKDIR: %s\n' "$PWD" > "$log_file"
printf 'COMMAND:' >> "$log_file"
printf ' %q' "$@" >> "$log_file"
printf '\n' >> "$log_file"

set +e
"$@" > "$tmp_file" 2>&1
command_status=$?
set -e

printf 'EXIT_STATUS: %s\n' "$command_status" >> "$log_file"
output_lines=$(wc -l < "$tmp_file")
printf 'OUTPUT_LINES: %s\n' "$output_lines" >> "$log_file"
printf '%s\n' '--- OUTPUT (bounded) ---' >> "$log_file"
if (( output_lines <= 320 )); then
  sed -n '1,320p' "$tmp_file" >> "$log_file"
else
  sed -n '1,160p' "$tmp_file" >> "$log_file"
  printf '%s\n' '--- OMITTED MIDDLE ---' >> "$log_file"
  tail -n 160 "$tmp_file" >> "$log_file"
fi

rm -f -- "$tmp_file"
exit "$command_status"
