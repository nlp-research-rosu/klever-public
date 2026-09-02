#!/usr/bin/env bash
set -u

run_cmd() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

run_shell() {
  local command_text="$1"
  printf '\n$ bash -lc %q\n' "$command_text"
  bash -lc "$command_text"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}
