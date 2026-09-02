#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s OUTPUT COMMAND [ARG ...]\n' "$0" >&2
  exit 2
fi

output_file=$1
shift

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$output_file"

set +e
"$@" 2>&1 | tee -a "$output_file"
command_status=${PIPESTATUS[0]}
set -e

printf 'EXIT_CODE: %d\n' "$command_status" | tee -a "$output_file"
exit "$command_status"
