#!/usr/bin/env bash
set -uo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift
tmp=$(mktemp /tmp/audit-log.XXXXXX)

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log"

"$@" > "$tmp" 2>&1
status=$?
line_count=$(wc -l < "$tmp")

{
  printf 'EXIT_STATUS: %s\n' "$status"
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  if [ "$line_count" -le 400 ]; then
    sed -n '1,400p' "$tmp"
  else
    printf '%s\n' '--- FIRST 240 LINES (bounded log) ---'
    sed -n '1,240p' "$tmp"
    printf '%s\n' '--- LAST 160 LINES (bounded log) ---'
    tail -n 160 "$tmp"
  fi
} >> "$log"

rm -f -- "$tmp"
exit "$status"
