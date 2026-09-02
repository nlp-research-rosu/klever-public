#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_dir=/audit-output/evidence/commands
capture_file=/tmp/audit-work/work/"${log_name}".capture
log_file="${log_dir}/${log_name}.log"
mkdir -p "$log_dir"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_file"

start_epoch=$(date +%s)
"$@" >"$capture_file" 2>&1
command_status=$?
end_epoch=$(date +%s)
line_count=$(wc -l <"$capture_file")
byte_count=$(wc -c <"$capture_file")

{
  printf 'EXIT_STATUS: %d\n' "$command_status"
  printf 'DURATION_SECONDS: %d\n' "$((end_epoch - start_epoch))"
  printf 'CAPTURE_LINES: %d\n' "$line_count"
  printf 'CAPTURE_BYTES: %d\n' "$byte_count"
  if (( line_count <= 800 )); then
    printf '%s\n' 'OUTPUT_BEGIN'
    sed -n '1,800p' "$capture_file"
    printf '%s\n' 'OUTPUT_END'
  else
    printf '%s\n' 'OUTPUT_HEAD_BEGIN'
    sed -n '1,400p' "$capture_file"
    printf '%s\n' 'OUTPUT_HEAD_END'
    printf '%s\n' 'OUTPUT_TRUNCATED_MIDDLE'
    printf '%s\n' 'OUTPUT_TAIL_BEGIN'
    tail -n 400 "$capture_file"
    printf '%s\n' 'OUTPUT_TAIL_END'
  fi
} >>"$log_file"

cat "$log_file"
exit "$command_status"
