#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift
tmp_path=$(mktemp /tmp/audit-command.XXXXXX)

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
  sed -n '1,2000p' "$tmp_path"
  line_count=$(wc -l <"$tmp_path")
  if (( line_count > 2000 )); then
    printf '%s\n' "--- OUTPUT TRUNCATED: ${line_count} total lines; first 2000 preserved ---"
  fi
  printf '%s\n' '--- END OUTPUT ---'
  printf 'EXIT STATUS: %d\n' "$command_status"
} | tee "$log_path"

rm -f -- "$tmp_path"
exit "$command_status"
