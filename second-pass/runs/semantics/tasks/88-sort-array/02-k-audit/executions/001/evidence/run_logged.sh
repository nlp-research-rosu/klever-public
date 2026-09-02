#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LOG_NAME COMMAND [ARG ...]\n' "$0" >&2
  exit 2
fi

log_name=$1
shift
evidence_dir=$(cd "$(dirname "$0")" && pwd)
log_path="$evidence_dir/$log_name"
tmp_path=$(mktemp /tmp/audit-work/audit-command.XXXXXX)

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_path"

"$@" >"$tmp_path" 2>&1
cmd_status=$?
line_count=$(wc -l <"$tmp_path")

{
  printf 'EXIT_STATUS: %s\n' "$cmd_status"
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  if (( line_count <= 500 )); then
    printf '%s\n' '--- OUTPUT (complete) ---'
    sed -n '1,500p' "$tmp_path"
  else
    printf '%s\n' '--- OUTPUT (first 250 lines) ---'
    sed -n '1,250p' "$tmp_path"
    printf '%s\n' '--- OUTPUT OMITTED (bounded log) ---'
    printf '%s\n' '--- OUTPUT (last 250 lines) ---'
    tail -n 250 "$tmp_path"
  fi
} >>"$log_path"

sed -n '1,560p' "$log_path"
rm -f "$tmp_path"
exit "$cmd_status"
