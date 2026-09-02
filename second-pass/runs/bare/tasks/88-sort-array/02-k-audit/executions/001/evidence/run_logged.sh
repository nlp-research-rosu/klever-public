#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
evidence_root=/audit-output/evidence
log_path="${evidence_root}/${log_name}.log"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_path"

set +e
"$@" >>"$log_path" 2>&1
status=$?
set -e

printf 'EXIT_STATUS: %d\n' "$status" >>"$log_path"
sed -n '1,240p' "$log_path"
exit "$status"
