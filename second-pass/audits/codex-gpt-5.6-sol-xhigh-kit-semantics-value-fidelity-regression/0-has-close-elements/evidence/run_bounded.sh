#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 2
fi

logfile=$1
shift
capture=$(mktemp /tmp/audit-work/audit-command.XXXXXX)

set +e
"$@" >"$capture" 2>&1
status=$?
set -e

line_count=$(wc -l <"$capture")
byte_count=$(wc -c <"$capture")

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'CAPTURED_LINES: %s\n' "$line_count"
  printf 'CAPTURED_BYTES: %s\n' "$byte_count"
  if (( line_count <= 400 )); then
    sed -n '1,400p' "$capture"
  else
    sed -n '1,200p' "$capture"
    printf '%s\n' '... [middle output omitted by reviewer; first/last 200 lines retained] ...'
    tail -n 200 "$capture"
  fi
  printf 'EXIT_STATUS: %s\n' "$status"
} >"$logfile"

sed -n '1,460p' "$logfile"
rm -f -- "$capture"
exit "$status"
