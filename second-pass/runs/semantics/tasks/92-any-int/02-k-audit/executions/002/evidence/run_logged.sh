#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}.log"
tmp_path=$(mktemp /tmp/audit-log.XXXXXX)

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
} > "$log_path"

"$@" > "$tmp_path" 2>&1
status=$?

{
  printf 'EXIT_STATUS: %d\n' "$status"
  printf '%s\n' 'OUTPUT_BEGIN'
  sed -n '1,1200p' "$tmp_path"
  printf '%s\n' 'OUTPUT_END'
} >> "$log_path"

sed -n '1,1200p' "$tmp_path"
printf 'EXIT_STATUS: %d\n' "$status"
rm -f "$tmp_path"
exit "$status"
