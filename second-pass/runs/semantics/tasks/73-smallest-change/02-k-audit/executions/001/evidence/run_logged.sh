#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

logfile=$1
shift

case "$logfile" in
  /audit-output/evidence/*) ;;
  *)
    echo "refusing log path outside /audit-output/evidence: $logfile" >&2
    exit 64
    ;;
esac

tmpfile=$(mktemp /tmp/audit-log.XXXXXX)
{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$logfile"

"$@" > "$tmpfile" 2>&1
status=$?
line_count=$(wc -l < "$tmpfile")

{
  printf 'EXIT_STATUS: %s\n' "$status"
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  if (( line_count <= 400 )); then
    sed -n '1,400p' "$tmpfile"
  else
    echo '--- FIRST 200 LINES (bounded log) ---'
    sed -n '1,200p' "$tmpfile"
    echo '--- LAST 200 LINES (bounded log) ---'
    tail -n 200 "$tmpfile"
  fi
} >> "$logfile"

rm -f -- "$tmpfile"
cat "$logfile"
exit "$status"
