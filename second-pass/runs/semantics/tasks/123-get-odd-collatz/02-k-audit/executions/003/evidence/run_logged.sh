#!/usr/bin/env bash
set +e

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift
tmp_path=$(mktemp /tmp/audit-work/command-output.XXXXXX)

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_path"

"$@" > "$tmp_path" 2>&1
command_status=$?
output_lines=$(wc -l < "$tmp_path")
output_bytes=$(wc -c < "$tmp_path")

{
  printf 'EXIT_STATUS: %s\n' "$command_status"
  printf 'OUTPUT_LINES: %s\n' "$output_lines"
  printf 'OUTPUT_BYTES: %s\n' "$output_bytes"
  printf '%s\n' '--- OUTPUT (bounded to first 800 and last 80 lines) ---'
  if (( output_lines <= 880 )); then
    sed -n '1,880p' "$tmp_path"
  else
    sed -n '1,800p' "$tmp_path"
    printf '%s\n' '--- [middle omitted] ---'
    tail -n 80 "$tmp_path"
  fi
} >> "$log_path"

sed -n '1,220p' "$log_path"
rm -f -- "$tmp_path"
exit "$command_status"
