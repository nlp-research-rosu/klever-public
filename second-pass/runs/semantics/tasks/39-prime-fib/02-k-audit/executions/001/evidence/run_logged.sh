#!/usr/bin/env bash
set -uo pipefail

if (( $# < 3 )); then
  echo "usage: run_logged.sh LABEL WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
run_dir=$2
shift 2
log="/audit-output/evidence/${label}.log"

{
  printf 'WORKDIR: %q\n' "$run_dir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log"

(
  cd "$run_dir" || exit 65
  "$@"
) 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log"
exit "$status"
