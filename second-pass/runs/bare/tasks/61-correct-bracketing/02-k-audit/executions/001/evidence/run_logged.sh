#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: run_logged.sh LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

audit_label=$1
shift
audit_log="/audit-output/evidence/${audit_label}.log"
audit_tmp="/tmp/audit-work/${audit_label}.full.log"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$audit_log"

"$@" > "$audit_tmp" 2>&1
audit_status=$?
audit_lines=$(wc -l < "$audit_tmp")

{
  printf 'EXIT_STATUS: %d\n' "$audit_status"
  printf 'OUTPUT_LINES: %d\n' "$audit_lines"
  printf '%s\n' '--- OUTPUT ---'
  if [ "$audit_lines" -le 400 ]; then
    sed -n '1,400p' "$audit_tmp"
  else
    sed -n '1,200p' "$audit_tmp"
    printf '%s\n' "--- OMITTED $((audit_lines - 400)) MIDDLE LINES ---"
    tail -n 200 "$audit_tmp"
  fi
} >> "$audit_log"

sed -n '1,80p' "$audit_log"
if [ "$audit_lines" -gt 80 ]; then
  printf 'Console output truncated; bounded record: %s\n' "$audit_log"
fi
exit "$audit_status"
