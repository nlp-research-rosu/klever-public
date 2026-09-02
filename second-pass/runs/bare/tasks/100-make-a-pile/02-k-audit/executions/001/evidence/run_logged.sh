#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift
tmp_log=$(mktemp /tmp/audit-work/command-log.XXXXXX)

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_path"

"$@" >"$tmp_log" 2>&1
command_status=$?
line_count=$(wc -l <"$tmp_log")

{
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  if [[ "$line_count" -le 500 ]]; then
    cat "$tmp_log"
  else
    sed -n '1,250p' "$tmp_log"
    printf '\n[... bounded log: middle omitted ...]\n\n'
    tail -n 250 "$tmp_log"
  fi
  printf 'EXIT_STATUS: %s\n' "$command_status"
} >>"$log_path"

rm -f -- "$tmp_log"
exit "$command_status"
