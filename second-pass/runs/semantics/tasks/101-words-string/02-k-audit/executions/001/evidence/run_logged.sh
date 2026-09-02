#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_PATH COMMAND [ARG ...]" >&2
  exit 2
fi

log_path=$1
shift
tmp_path="${log_path}.tmp"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >"$tmp_path"

set +e
"$@" >>"$tmp_path" 2>&1
status=$?
set -e

{
  printf 'EXIT_STATUS: %d\n' "$status"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >>"$tmp_path"

mv "$tmp_path" "$log_path"
sed -n '1,240p' "$log_path"
line_count=$(wc -l <"$log_path")
if (( line_count > 240 )); then
  printf '[display truncated; full bounded command log has %d lines at %s]\n' \
    "$line_count" "$log_path"
fi
exit "$status"
