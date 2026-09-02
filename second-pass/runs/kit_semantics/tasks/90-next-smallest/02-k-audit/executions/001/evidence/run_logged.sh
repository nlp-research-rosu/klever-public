#!/usr/bin/env bash
set -u

if [ "$#" -lt 2 ]; then
  echo "usage: run_logged.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift

{
  echo "COMMAND (shell-escaped):"
  printf ' %q' "$@"
  echo
  echo "WORKDIR: $(pwd)"
  echo "START_UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "OUTPUT:"
} > "$log_file"

"$@" >> "$log_file" 2>&1
status=$?

{
  echo
  echo "EXIT_STATUS: $status"
  echo "END_UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$log_file"

cat "$log_file"
exit "$status"
