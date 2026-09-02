#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOGFILE COMMAND [ARG ...]" >&2
  exit 2
fi

logfile=$1
shift
capture_file=$(mktemp /tmp/audit-log-capture.XXXXXX)
trap 'rm -f "$capture_file"' EXIT

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
} > "$logfile"

"$@" >"$capture_file" 2>&1
status=$?
tee -a "$logfile" <"$capture_file"
printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$logfile"
exit "$status"
