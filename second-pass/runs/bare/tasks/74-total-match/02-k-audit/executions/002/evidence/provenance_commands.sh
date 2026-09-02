#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  return 0
}

run ls -ld /audit-input.json /audit-campaign-lock.json /run.json /task.json \
  /generation-result.json /candidate /reference /generation-evidence
run sha256sum /audit-input.json /audit-campaign-lock.json /run.json /task.json \
  /generation-result.json
run sed -n 1,320p /audit-input.json
run sed -n 1,320p /audit-campaign-lock.json
