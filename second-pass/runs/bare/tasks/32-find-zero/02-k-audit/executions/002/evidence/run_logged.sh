#!/usr/bin/env bash
# Reviewer-authored command logger. Usage:
#   run_logged.sh LOGFILE COMMAND [ARG ...]
set +e

log_file=$1
shift

{
  printf 'CWD: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf '%s\n' '--- OUTPUT BEGIN ---'
  "$@"
  command_status=$?
  printf '%s\n' '--- OUTPUT END ---'
  printf 'EXIT STATUS: %d\n' "$command_status"
  exit "$command_status"
} >"$log_file" 2>&1
