#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_PATH COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift
tmp_path=$(mktemp /tmp/audit-work/command-output.XXXXXX)

set +e
"$@" >"$tmp_path" 2>&1
command_status=$?
set -e

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '--- OUTPUT ---'
  sed -n '1,1200p' "$tmp_path"
  output_lines=$(wc -l <"$tmp_path")
  if (( output_lines > 1200 )); then
    printf '%s\n' "--- OUTPUT TRUNCATED: ${output_lines} total lines ---"
  fi
  printf '%s\n' '--- STATUS ---'
  printf 'EXIT: %d\n' "$command_status"
} | tee "$log_path"

rm -f "$tmp_path"
exit "$command_status"
