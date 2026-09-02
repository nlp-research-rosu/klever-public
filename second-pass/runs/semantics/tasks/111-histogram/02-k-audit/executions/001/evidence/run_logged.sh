#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 3 ]]; then
  echo "usage: run_logged.sh LABEL WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

label="$1"
workdir="$2"
shift 2
log_dir="/audit-output/evidence/logs"
log_path="${log_dir}/${label}.log"
mkdir -p "$log_dir"

{
  printf 'WORKDIR: %s\n' "$workdir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_path"

set +e
(
  cd "$workdir" || exit 125
  "$@"
) 2>&1 | tee -a "$log_path"
status=${PIPESTATUS[0]}
set -e

printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$log_path"
exit "$status"
