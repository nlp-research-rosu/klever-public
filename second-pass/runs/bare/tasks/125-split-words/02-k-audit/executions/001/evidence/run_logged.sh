#!/usr/bin/env bash
set -uo pipefail

if (( $# < 3 )); then
  echo "usage: run_logged.sh LOG_NAME MAX_LINES COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
max_lines=$2
shift 2

case "$log_name" in
  *[!A-Za-z0-9._-]*|'')
    echo "invalid log name: $log_name" >&2
    exit 64
    ;;
esac

if ! [[ "$max_lines" =~ ^[0-9]+$ ]] || (( max_lines < 20 )); then
  echo "MAX_LINES must be an integer of at least 20" >&2
  exit 64
fi

evidence_dir=/audit-output/evidence
scratch_log_dir=/tmp/audit-work/logs
mkdir -p "$evidence_dir" "$scratch_log_dir"
raw_log=$(mktemp "$scratch_log_dir/${log_name}.raw.XXXXXX")
final_log="$evidence_dir/$log_name"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$final_log"

set +e
timeout 1800 "$@" >"$raw_log" 2>&1
cmd_status=$?
set -e

line_count=$(wc -l <"$raw_log")
{
  printf 'EXIT_STATUS: %s\n' "$cmd_status"
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  printf '%s\n' '--- OUTPUT BEGIN ---'
  if (( line_count <= max_lines )); then
    sed -n "1,${max_lines}p" "$raw_log"
  else
    head_lines=$((max_lines * 2 / 3))
    tail_lines=$((max_lines - head_lines))
    sed -n "1,${head_lines}p" "$raw_log"
    printf '%s\n' "--- OUTPUT TRUNCATED: omitted $((line_count - max_lines)) lines ---"
    tail -n "$tail_lines" "$raw_log"
  fi
  printf '%s\n' '--- OUTPUT END ---'
} >>"$final_log"

sed -n '1,80p' "$final_log"
exit "$cmd_status"
