#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  printf 'usage: %s LABEL COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

label=$1
shift
if [[ ! $label =~ ^[A-Za-z0-9._-]+$ ]]; then
  printf 'invalid log label: %s\n' "$label" >&2
  exit 64
fi

log="/audit-output/evidence/${label}.log"
{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log"

set -o pipefail
"$@" 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log"
exit "$status"
