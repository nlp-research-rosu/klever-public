#!/usr/bin/env bash
# Run one command, preserving its exact argv, bounded output, and exit status.
set -u

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LOG_PATH COMMAND [ARG ...]\n' "$0" >&2
  exit 2
fi

log_path=$1
shift
raw_log=$(mktemp /tmp/audit-command.XXXXXX)

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$raw_log"

"$@" >> "$raw_log" 2>&1
command_status=$?
printf '\nEXIT_STATUS: %d\n' "$command_status" >> "$raw_log"

raw_size=$(wc -c < "$raw_log")
if [[ "$raw_size" -le 120000 ]]; then
  cp "$raw_log" "$log_path"
else
  {
    head -c 80000 "$raw_log"
    printf '\n... OUTPUT BOUNDED: %d total bytes; middle omitted ...\n' "$raw_size"
    tail -c 40000 "$raw_log"
  } > "$log_path"
fi

rm -f "$raw_log"
sed -n '1,260p' "$log_path"
exit "$command_status"
