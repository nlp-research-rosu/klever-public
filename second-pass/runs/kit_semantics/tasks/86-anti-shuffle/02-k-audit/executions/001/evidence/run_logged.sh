#!/usr/bin/env bash
# Run one command and preserve a bounded, reproducible combined-output log.
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log_path=$1
shift
tmp_log=$(mktemp /tmp/audit-work/anti-shuffle-command.XXXXXX)
trap 'rm -f -- "$tmp_log"' EXIT

"$@" >"$tmp_log" 2>&1
status=$?
line_count=$(wc -l <"$tmp_log")
byte_count=$(wc -c <"$tmp_log")

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\nEXIT: %s\nOUTPUT_LINES: %s\nOUTPUT_BYTES: %s\nOUTPUT:\n' \
    "$status" "$line_count" "$byte_count"
  if (( line_count <= 240 )); then
    sed -n '1,240p' "$tmp_log"
  else
    sed -n '1,120p' "$tmp_log"
    printf '\n[... %s middle lines omitted ...]\n\n' "$((line_count - 240))"
    tail -n 120 "$tmp_log"
  fi
} >"$log_path"

exit "$status"
