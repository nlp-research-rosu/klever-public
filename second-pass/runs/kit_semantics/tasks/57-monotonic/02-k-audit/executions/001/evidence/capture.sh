#!/usr/bin/env bash
set -uo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: capture.sh LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
shift
log_dir=$(cd "$(dirname "$0")" && pwd)
log_file="$log_dir/$label.log"

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  exit "$status"
} >"$log_file" 2>&1
