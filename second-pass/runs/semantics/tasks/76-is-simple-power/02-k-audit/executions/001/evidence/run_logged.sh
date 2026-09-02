#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift
tmp_path=$(mktemp /tmp/audit-command-output.XXXXXX)

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_path"

set +e
"$@" > "$tmp_path" 2>&1
command_status=$?
set -e

tee -a "$log_path" < "$tmp_path"
printf '\nEXIT_STATUS: %d\n' "$command_status" | tee -a "$log_path"
rm -f -- "$tmp_path"
exit "$command_status"
