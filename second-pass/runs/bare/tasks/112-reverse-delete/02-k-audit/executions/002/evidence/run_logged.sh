#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LOG_PATH COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_path=$1
shift
tmp_output=$(mktemp /tmp/audit-command-output.XXXXXX)

set +e
"$@" >"$tmp_output" 2>&1
command_status=$?
set -e

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\nEXIT STATUS: %d\n' "$command_status"
  printf '%s\n' 'OUTPUT (bounded to first 220 and last 80 lines):'
  total_lines=$(wc -l <"$tmp_output")
  if (( total_lines <= 300 )); then
    sed -n '1,300p' "$tmp_output"
  else
    sed -n '1,220p' "$tmp_output"
    printf '\n... %d middle lines omitted ...\n\n' "$((total_lines - 300))"
    tail -n 80 "$tmp_output"
  fi
} >"$log_path"

rm -f "$tmp_output"
exit "$command_status"
