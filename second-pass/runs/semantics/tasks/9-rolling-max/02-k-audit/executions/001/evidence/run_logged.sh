#!/usr/bin/env bash
set -u

if [[ $# -lt 3 ]]; then
  echo "usage: $0 LOG_FILE WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
work_dir=$2
shift 2

{
  printf 'WORKDIR: %s\n' "$work_dir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_file"

(
  cd "$work_dir" || exit 72
  "$@"
) > >(tee -a "$log_file") 2> >(tee -a "$log_file" >&2)
status=$?
printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log_file"
exit "$status"
