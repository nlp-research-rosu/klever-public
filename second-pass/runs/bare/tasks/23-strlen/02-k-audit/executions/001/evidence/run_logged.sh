#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
shift
raw=$(mktemp /tmp/audit-work/audit-command.XXXXXX)

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log"

"$@" > "$raw" 2>&1
status=$?
lines=$(wc -l < "$raw")

{
  printf 'EXIT_STATUS: %d\n' "$status"
  printf 'OUTPUT_LINES: %d\n' "$lines"
  printf '%s\n' '--- OUTPUT ---'
  if (( lines <= 320 )); then
    sed -n '1,320p' "$raw"
  else
    sed -n '1,240p' "$raw"
    printf '%s\n' "--- OMITTED $((lines - 320)) MIDDLE LINES ---"
    tail -n 80 "$raw"
  fi
  printf '%s\n' '--- END OUTPUT ---'
} >> "$log"

rm -f "$raw"
exit "$status"
