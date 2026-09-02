#!/usr/bin/env bash
set -u

if [[ $# -lt 3 ]]; then
  echo "usage: run_logged.sh LOG_FILE WORKDIR COMMAND..." >&2
  exit 64
fi

log_file=$1
work_dir=$2
shift 2
command_text=$*
capture_file=$(mktemp /tmp/55-fib-audit-log.XXXXXX)

{
  printf 'WORKDIR: %s\n' "$work_dir"
  printf 'COMMAND: %s\n' "$command_text"
} >"$log_file"

(
  cd "$work_dir" || exit 200
  bash -o pipefail -c "$command_text"
) >"$capture_file" 2>&1
command_status=$?
line_count=$(wc -l <"$capture_file")

{
  printf 'EXIT_STATUS: %s\n' "$command_status"
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  printf '%s\n' 'OUTPUT_BEGIN'
  if (( line_count <= 500 )); then
    sed -n '1,500p' "$capture_file"
  else
    sed -n '1,300p' "$capture_file"
    printf '%s\n' '... OUTPUT TRUNCATED: showing final 200 lines ...'
    tail -n 200 "$capture_file"
  fi
  printf '%s\n' 'OUTPUT_END'
} >>"$log_file"

rm -f "$capture_file"
exit "$command_status"
