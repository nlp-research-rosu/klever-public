#!/usr/bin/env bash
set -u

if [[ $# -ne 2 ]]; then
  echo "usage: run_logged.sh LOG_FILE COMMAND" >&2
  exit 2
fi

log_file=$1
command_text=$2

{
  printf 'COMMAND: %s\n' "$command_text"
  printf 'WORKDIR: %s\n' "$PWD"
  printf '%s\n' '--- OUTPUT BEGIN ---'
} >"$log_file"

set +e
bash -o pipefail -c "$command_text" >>"$log_file" 2>&1
command_status=$?
set -e

{
  printf '%s\n' '--- OUTPUT END ---'
  printf 'EXIT_STATUS: %d\n' "$command_status"
} >>"$log_file"

exit "$command_status"
