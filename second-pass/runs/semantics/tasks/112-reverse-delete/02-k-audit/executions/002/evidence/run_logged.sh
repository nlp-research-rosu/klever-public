#!/usr/bin/env bash
# Reviewer-authored command logger. Usage:
#   ./run_logged.sh LABEL COMMAND [ARG ...]
set -u

if [[ $# -lt 2 ]]; then
  printf 'usage: %s LABEL COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

label=$1
shift
log="/audit-output/evidence/${label}.log"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} | tee "$log"

"$@" 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log"
exit "$status"
