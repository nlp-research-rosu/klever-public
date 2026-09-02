#!/usr/bin/env bash
set -uo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift
audit_tmp="${audit_log}.tmp"

"$@" >"$audit_tmp" 2>&1
audit_status=$?

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '----- OUTPUT -----'
  sed -n '1,2000p' "$audit_tmp"
  printf '%s\n' '----- END OUTPUT -----'
  printf 'EXIT_STATUS: %s\n' "$audit_status"
} >"$audit_log"

rm -f "$audit_tmp"
sed -n '1,220p' "$audit_log"
exit "$audit_status"
