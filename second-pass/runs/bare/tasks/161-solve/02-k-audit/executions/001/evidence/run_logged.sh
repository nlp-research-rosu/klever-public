#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  printf 'usage: %s LOGFILE COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

logfile=$1
shift
tmpfile=$(mktemp /tmp/audit-work/audit-command.XXXXXX)

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$logfile"

"$@" > "$tmpfile" 2>&1
status=$?
line_count=$(wc -l < "$tmpfile")

if (( line_count <= 400 )); then
  sed -n '1,400p' "$tmpfile" >> "$logfile"
else
  sed -n '1,200p' "$tmpfile" >> "$logfile"
  printf '\n[... %d middle lines omitted by reviewer log bound ...]\n\n' "$((line_count - 400))" >> "$logfile"
  tail -n 200 "$tmpfile" >> "$logfile"
fi

printf 'EXIT_STATUS: %d\n' "$status" >> "$logfile"
rm -f "$tmpfile"
exit "$status"
