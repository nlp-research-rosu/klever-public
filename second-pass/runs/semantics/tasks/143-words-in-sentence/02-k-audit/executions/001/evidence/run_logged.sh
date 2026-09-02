#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 3 ]]; then
  echo "usage: run_logged.sh LOG WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
command_workdir=$2
shift 2

temporary_output=$(mktemp /tmp/audit-command-output.XXXXXX)
cleanup() {
  rm -f -- "$temporary_output"
}
trap cleanup EXIT

set +e
(
  cd -- "$command_workdir" &&
  "$@"
) >"$temporary_output" 2>&1
command_status=$?
set -e

output_bytes=$(wc -c <"$temporary_output")
{
  printf 'WORKDIR: %s\n' "$command_workdir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\nEXIT_STATUS: %s\n' "$command_status"
  printf 'OUTPUT_BYTES: %s\n' "$output_bytes"
  printf '%s\n' '--- OUTPUT ---'
  if (( output_bytes <= 200000 )); then
    sed -n '1,4000p' "$temporary_output"
  else
    head -c 100000 "$temporary_output"
    printf '\n%s\n' '--- OUTPUT TRUNCATED: middle omitted ---'
    tail -c 100000 "$temporary_output"
  fi
} >"$log_path"

cat -- "$log_path"
exit "$command_status"
