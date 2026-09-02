#!/usr/bin/env bash
set -uo pipefail

audit_log=$1
shift

{
  printf 'WORKDIR=%q\n' "$PWD"
  printf 'COMMAND='
  printf '%q ' "$@"
  printf '\n'
  "$@"
  audit_status=$?
  printf 'EXIT_STATUS=%d\n' "$audit_status"
} >"$audit_log" 2>&1

exit "$audit_status"
