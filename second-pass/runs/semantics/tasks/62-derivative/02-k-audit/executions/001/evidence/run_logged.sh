#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  printf 'usage: %s LOG_NAME COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_name=$1
shift
evidence_dir=/audit-output/evidence
raw_log=/tmp/audit-work/"${log_name}.raw.log"
final_log="${evidence_dir}/${log_name}.log"

mkdir -p "$evidence_dir" /tmp/audit-work

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$final_log"

"$@" > "$raw_log" 2>&1
status=$?

{
  printf 'EXIT_STATUS: %d\n' "$status"
  printf '%s\n' 'OUTPUT_BEGIN'
  line_count=$(wc -l < "$raw_log")
  if (( line_count <= 800 )); then
    sed -n '1,800p' "$raw_log"
  else
    sed -n '1,600p' "$raw_log"
    printf '%s\n' "... OUTPUT TRUNCATED: ${line_count} total lines; showing first 600 and last 200 ..."
    tail -n 200 "$raw_log"
  fi
  printf '%s\n' 'OUTPUT_END'
} >> "$final_log"

sed -n '1,1000p' "$final_log"
exit "$status"
