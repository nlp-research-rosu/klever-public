#!/usr/bin/env bash
set -uo pipefail

if (( $# < 3 )); then
  echo "usage: run_logged.sh LOG WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
run_dir=$2
shift 2
cmd=("$@")
tmp_path=$(mktemp /tmp/audit-work/audit-command.XXXXXX)
trap 'rm -f "$tmp_path"' EXIT

{
  printf 'WORKDIR: %q\n' "$run_dir"
  printf 'COMMAND:'
  printf ' %q' "${cmd[@]}"
  printf '\n'
} >"$log_path"

(
  cd "$run_dir" || exit 125
  "${cmd[@]}"
) >"$tmp_path" 2>&1
status=$?
line_count=$(wc -l <"$tmp_path")

{
  printf 'EXIT_STATUS: %d\n' "$status"
  printf 'OUTPUT_LINES: %d\n' "$line_count"
  if (( line_count <= 500 )); then
    printf '%s\n' '--- OUTPUT (complete) ---'
    sed -n '1,500p' "$tmp_path"
  else
    printf '%s\n' '--- OUTPUT (first 250 lines) ---'
    sed -n '1,250p' "$tmp_path"
    printf '%s\n' '--- OUTPUT (last 250 lines; middle omitted) ---'
    tail -n 250 "$tmp_path"
  fi
} >>"$log_path"

sed -n '1,80p' "$log_path"
if (( line_count > 80 )); then
  echo "[console preview truncated; bounded log contains recorded output]"
fi
exit "$status"
