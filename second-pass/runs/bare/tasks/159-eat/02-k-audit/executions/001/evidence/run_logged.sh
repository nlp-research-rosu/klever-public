#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  printf 'usage: %s LOGFILE COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

logfile=$1
shift
tmpfile=$(mktemp /tmp/audit-log.XXXXXX)

set +e
"$@" >"$tmpfile" 2>&1
status=$?
set -e

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\nEXIT_STATUS: %s\n' "$status"
  lines=$(wc -l <"$tmpfile")
  bytes=$(wc -c <"$tmpfile")
  printf 'OUTPUT_LINES: %s\nOUTPUT_BYTES: %s\n' "$lines" "$bytes"
  if (( lines <= 240 )); then
    printf '%s\n' '--- OUTPUT (complete) ---'
    sed -n '1,240p' "$tmpfile"
  else
    printf '%s\n' '--- OUTPUT (first 180 lines) ---'
    sed -n '1,180p' "$tmpfile"
    printf '%s\n' '--- OUTPUT (last 60 lines) ---'
    tail -n 60 "$tmpfile"
  fi
} >"$logfile"

sed -n '1,40p' "$logfile"
if (( lines > 40 )); then
  printf '[console output truncated; complete bounded record: %s]\n' "$logfile"
fi

rm -f -- "$tmpfile"
exit "$status"
