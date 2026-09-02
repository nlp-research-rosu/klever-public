#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_BASENAME COMMAND [ARG ...]" >&2
  exit 2
fi

log_base="$1"
shift
log_path="/audit-output/evidence/${log_base}.log"
status_path="/audit-output/evidence/${log_base}.status"

(
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf '\nEXIT_STATUS: %d\n' "$command_status"
  exit "$command_status"
) >"$log_path" 2>&1
command_status=$?
printf '%d\n' "$command_status" >"$status_path"

sed -n '1,260p' "$log_path"
line_count="$(wc -l <"$log_path")"
if (( line_count > 260 )); then
  printf '\n[log display truncated; complete bounded log at %s, %d lines]\n' \
    "$log_path" "$line_count"
fi
exit "$command_status"
