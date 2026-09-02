#!/usr/bin/env bash
set -u

if [[ "$#" -lt 3 ]]; then
  echo "usage: run_logged.sh LABEL WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

label="$1"
run_directory="$2"
shift 2
log="/audit-output/evidence/logs/${label}.log"

{
  printf 'cwd: %s\n' "$run_directory"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n--- output ---\n'
} >"$log"

(
  cd "$run_directory" || exit 125
  "$@"
) >>"$log" 2>&1
status=$?

{
  printf '%s\n' '--- end output ---'
  printf 'exit_status: %s\n' "$status"
} >>"$log"

cat "$log"
exit "$status"
