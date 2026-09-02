#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -ne 2 ]]; then
  printf 'usage: %s LOGFILE SHELL_COMMAND\n' "$0" >&2
  exit 64
fi

log_file="$1"
shell_command="$2"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND: bash -lc %q\n' "$shell_command"
} | tee "$log_file"

bash -lc "$shell_command" 2>&1 | tee -a "$log_file"
command_status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %d\n' "$command_status" | tee -a "$log_file"
exit "$command_status"
