#!/usr/bin/env bash
set -uo pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_PREFIX COMMAND [ARG ...]" >&2
  exit 2
fi

log_prefix=$1
shift

{
  printf 'cwd: %q\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
} > "${log_prefix}.command"

set +e
"$@" > >(tee "${log_prefix}.log") 2>&1
status=$?
set -e

printf '%s\n' "$status" > "${log_prefix}.exit"
printf 'exit_status=%s\n' "$status" | tee -a "${log_prefix}.log"
exit "$status"
