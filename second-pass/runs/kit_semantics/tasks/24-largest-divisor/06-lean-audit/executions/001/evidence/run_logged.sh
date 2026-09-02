#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

if (( $# < 2 )); then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 2
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'BEGIN OUTPUT\n'
} > "$log_path"

set +o errexit
"$@" > >(tee -a "$log_path") 2> >(tee -a "$log_path" >&2)
command_status=$?
set -o errexit

{
  printf '\nEND OUTPUT\n'
  printf 'EXIT CODE: %d\n' "$command_status"
} >> "$log_path"

exit "$command_status"
