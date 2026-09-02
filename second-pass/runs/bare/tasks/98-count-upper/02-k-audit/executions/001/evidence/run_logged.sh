#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG_BASENAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
evidence_dir=$(cd "$(dirname "$0")" && pwd)
raw_file=$(mktemp /tmp/audit-command.XXXXXX)
log_file="$evidence_dir/$log_name.log"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_file"

set +e
"$@" >"$raw_file" 2>&1
command_status=$?
set -e

line_count=$(wc -l <"$raw_file")
byte_count=$(wc -c <"$raw_file")
{
  printf 'EXIT_STATUS: %s\n' "$command_status"
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  printf 'OUTPUT_BYTES: %s\n' "$byte_count"
  printf '%s\n' '--- OUTPUT ---'
  if (( line_count <= 2000 )); then
    sed -n '1,2000p' "$raw_file"
  else
    sed -n '1,1000p' "$raw_file"
    printf '%s\n' "--- TRUNCATED $((line_count - 2000)) MIDDLE LINES ---"
    tail -n 1000 "$raw_file"
  fi
} >>"$log_file"

rm -f "$raw_file"
cat "$log_file"
exit "$command_status"
