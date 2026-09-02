#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  printf 'usage: %s LABEL COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

label=$1
shift
log_dir=/audit-output/evidence
log_path="$log_dir/$label.log"

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_path"

"$@" >>"$log_path" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status" >>"$log_path"
exit "$status"
