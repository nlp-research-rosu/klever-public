#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: run_bounded.sh LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log_path=$1
shift
tmp_path=$(mktemp /tmp/audit-command.XXXXXX)

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
} > "$log_path"

"$@" > "$tmp_path" 2>&1
command_status=$?
line_count=$(wc -l < "$tmp_path")
byte_count=$(wc -c < "$tmp_path")

{
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  printf 'OUTPUT_BYTES: %s\n' "$byte_count"
  if [ "$line_count" -le 500 ]; then
    sed -n '1,500p' "$tmp_path"
  else
    printf '%s\n' '[first 250 lines]'
    sed -n '1,250p' "$tmp_path"
    printf '%s\n' "[... $((line_count - 500)) lines omitted ...]"
    printf '%s\n' '[last 250 lines]'
    tail -n 250 "$tmp_path"
  fi
  printf 'EXIT_STATUS: %s\n' "$command_status"
} >> "$log_path"

rm -f "$tmp_path"
exit "$command_status"
