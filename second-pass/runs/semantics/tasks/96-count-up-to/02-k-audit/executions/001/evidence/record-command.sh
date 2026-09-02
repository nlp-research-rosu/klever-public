#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
shift
log_dir=$(cd "$(dirname "$0")" && pwd)
log_path="$log_dir/$label.log"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_path"

set +e
"$@" >"$log_path.output" 2>&1
status=$?
set -e

{
  printf 'EXIT_STATUS: %d\n' "$status"
  printf '%s\n' '--- OUTPUT (first 240 lines) ---'
  sed -n '1,240p' "$log_path.output"
  lines=$(wc -l <"$log_path.output")
  if (( lines > 240 )); then
    printf '%s\n' "--- OUTPUT TRUNCATED: $lines total lines; last 40 lines follow ---"
    tail -n 40 "$log_path.output"
  fi
} >>"$log_path"

rm -f "$log_path.output"
cat "$log_path"
exit "$status"
