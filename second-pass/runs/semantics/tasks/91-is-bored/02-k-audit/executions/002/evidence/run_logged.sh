#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -ne 3 ]]; then
  echo "usage: run_logged.sh LABEL WORKDIR COMMAND" >&2
  exit 64
fi

label="$1"
command_workdir="$2"
command_text="$3"
log="/audit-output/evidence/${label}.log"

{
  printf 'WORKDIR: %s\n' "$command_workdir"
  printf 'COMMAND: %s\n' "$command_text"
  printf '%s\n' '--- OUTPUT ---'
  (
    cd "$command_workdir" || exit 125
    bash -lc "$command_text"
  )
  status=$?
  printf '%s\n' '--- STATUS ---'
  printf 'EXIT_STATUS: %s\n' "$status"
  exit "$status"
} >"$log" 2>&1
