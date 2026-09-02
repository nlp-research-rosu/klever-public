#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift
tmp_path=$(mktemp /tmp/audit-log.XXXXXX)

set +e
"$@" >"$tmp_path" 2>&1
command_status=$?
set -e

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\nEXIT_STATUS: %d\n' "$command_status"
  printf '%s\n' 'OUTPUT_BEGIN'
  output_bytes=$(wc -c <"$tmp_path")
  if [[ "$output_bytes" -le 200000 ]]; then
    sed -n '1,$p' "$tmp_path"
  else
    printf 'OUTPUT_TRUNCATED: %s bytes; first and last 1000 lines retained\n' "$output_bytes"
    sed -n '1,1000p' "$tmp_path"
    printf '%s\n' '... TRUNCATED MIDDLE ...'
    tail -n 1000 "$tmp_path"
  fi
  printf '%s\n' 'OUTPUT_END'
} >"$log_path"

rm -f -- "$tmp_path"
exit "$command_status"
