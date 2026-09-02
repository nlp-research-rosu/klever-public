#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log_path=$1
shift
tmp_path=$(mktemp /tmp/audit-log.XXXXXX)

{
  printf 'cwd: %q\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
} >"$tmp_path"

"$@" >>"$tmp_path" 2>&1
command_status=$?
printf 'exit_status: %d\n' "$command_status" >>"$tmp_path"
cp "$tmp_path" "$log_path"
sed -n '1,1200p' "$tmp_path"
rm -f "$tmp_path"
exit "$command_status"
