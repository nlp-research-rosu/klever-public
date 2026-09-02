#!/usr/bin/env bash
set -o pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  "$@"
  audit_status=$?
  printf 'EXIT_STATUS: %d\n' "$audit_status"
  exit "$audit_status"
} 2>&1 | tee "$audit_log"
