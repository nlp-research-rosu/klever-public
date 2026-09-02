#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LABEL COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

label="$1"
shift
log="/audit-output/evidence/${label}.log"

{
  printf 'cwd=%q\n' "$PWD"
  printf 'command='
  printf '%q ' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'exit_status=%d\n' "$status"
  exit "$status"
} >"$log" 2>&1
