#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: run_bounded.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift
tmp_path=$(mktemp /tmp/audit-work/audit-command.XXXXXX)

set +e
"$@" >"$tmp_path" 2>&1
status=$?
set -e

line_count=$(wc -l <"$tmp_path")
byte_count=$(wc -c <"$tmp_path")
{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'EXIT_STATUS: %s\n' "$status"
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  printf 'OUTPUT_BYTES: %s\n' "$byte_count"
  if (( line_count <= 320 )); then
    cat "$tmp_path"
  else
    echo "--- first 160 lines (bounded log) ---"
    head -n 160 "$tmp_path"
    echo "--- last 160 lines (bounded log) ---"
    tail -n 160 "$tmp_path"
  fi
} >"$log_path"

rm -f -- "$tmp_path"
exit "$status"
