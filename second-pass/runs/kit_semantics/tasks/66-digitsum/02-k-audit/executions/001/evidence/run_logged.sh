#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}"
tmp_path=$(mktemp /tmp/audit-work/command-output.XXXXXX)

set +e
"$@" >"$tmp_path" 2>&1
status=$?
set -e

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\nEXIT_STATUS: %d\nOUTPUT:\n' "$status"
  sed -n '1,400p' "$tmp_path"
} >"$log_path"

sed -n '1,400p' "$log_path"
exit "$status"
