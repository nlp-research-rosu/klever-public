#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

evidence_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
log_name="$1"
shift
log_path="${evidence_dir}/${log_name}"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf '%s\n' '----- OUTPUT -----'
} >"$log_path"

"$@" >>"$log_path" 2>&1
command_status=$?

{
  printf '%s\n' '----- END OUTPUT -----'
  printf 'EXIT STATUS: %d\n' "$command_status"
} >>"$log_path"

cat "$log_path"
exit "$command_status"
