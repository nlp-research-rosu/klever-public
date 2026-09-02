#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  echo "usage: run_logged.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path="$1"
shift
tmp_output="$(mktemp /tmp/audit-command.XXXXXX)"

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_path"

set +e
"$@" > "$tmp_output" 2>&1
command_status=$?
set -e

tee -a "$log_path" < "$tmp_output"
printf 'EXIT_STATUS: %d\n' "$command_status" | tee -a "$log_path"
rm -f -- "$tmp_output"
exit "$command_status"
