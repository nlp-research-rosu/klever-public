#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}.log"
tmp_path=$(mktemp /tmp/audit-work/audit-command.XXXXXX)

{
  printf 'cwd: %q\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
  printf 'started_utc: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$log_path"

"$@" > "$tmp_path" 2>&1
status=$?
line_count=$(wc -l < "$tmp_path")
byte_count=$(wc -c < "$tmp_path")

{
  printf 'exit_status: %d\n' "$status"
  printf 'output_lines: %d\n' "$line_count"
  printf 'output_bytes: %d\n' "$byte_count"
  printf '%s\n' '--- output (complete when <= 600 lines; otherwise first/last 300) ---'
  if (( line_count <= 600 )); then
    sed -n '1,600p' "$tmp_path"
  else
    sed -n '1,300p' "$tmp_path"
    printf '%s\n' '--- bounded log: middle omitted ---'
    tail -n 300 "$tmp_path"
  fi
} >> "$log_path"

rm -f -- "$tmp_path"
exit "$status"
