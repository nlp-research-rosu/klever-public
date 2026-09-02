#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
evidence_dir=/audit-output/evidence
scratch_dir=/tmp/audit-work
mkdir -p "$evidence_dir" "$scratch_dir"
raw_output=$(mktemp "$scratch_dir/.audit-command.XXXXXX")
log_path="$evidence_dir/$log_name"

{
  printf 'PWD: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_path"

set +e
"$@" >"$raw_output" 2>&1
command_status=$?
set -e

line_count=$(wc -l <"$raw_output")
byte_count=$(wc -c <"$raw_output")
{
  printf 'EXIT_STATUS: %d\n' "$command_status"
  printf 'OUTPUT_LINES: %d\n' "$line_count"
  printf 'OUTPUT_BYTES: %d\n' "$byte_count"
  printf '%s\n' '--- OUTPUT (bounded) ---'
  if (( line_count <= 500 )); then
    sed -n '1,500p' "$raw_output"
  else
    sed -n '1,350p' "$raw_output"
    printf '%s\n' "--- OMITTED $((line_count - 500)) MIDDLE LINES ---"
    tail -n 150 "$raw_output"
  fi
} >>"$log_path"

sed -n '1,350p' "$raw_output"
if (( line_count > 500 )); then
  printf '%s\n' "--- OMITTED $((line_count - 500)) MIDDLE LINES ---"
  tail -n 150 "$raw_output"
fi
printf 'EXIT_STATUS=%d\n' "$command_status"
rm -f "$raw_output"
exit "$command_status"
