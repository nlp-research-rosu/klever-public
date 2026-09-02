#!/usr/bin/env bash
set -u

if [[ "$#" -lt 3 ]]; then
  echo "usage: $0 LOG_FILE WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
work_dir=$2
shift 2

{
  printf 'WORKDIR: %q\n' "$work_dir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_file"

(
  cd "$work_dir" || exit 72
  "$@"
) >>"$log_file" 2>&1
status=$?

printf 'EXIT_STATUS: %d\n' "$status" >>"$log_file"
exit "$status"
