#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
shift
evidence_dir=$(cd "$(dirname "$0")" && pwd)
cmd_file="$evidence_dir/${label}.cmd"
log_file="$evidence_dir/${label}.log"
status_file="$evidence_dir/${label}.status"

{
  printf 'cwd=%q\n' "$PWD"
  printf 'command='
  printf '%q ' "$@"
  printf '\n'
} >"$cmd_file"

set +e
"$@" 2>&1 | tee "$log_file"
status=${PIPESTATUS[0]}
set -e
printf '%s\n' "$status" >"$status_file"
printf 'exit_status=%s\n' "$status"
exit "$status"
