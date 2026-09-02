#!/usr/bin/env bash
set -u

status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

run stat -c '%F %A %U:%G %n' \
  /audit-input.json /audit-campaign-lock.json /run.json /task.json \
  /generation-result.json /candidate /reference /generation-evidence
run find /candidate -maxdepth 3 -printf '%y %p -> %l\n'
run find /reference -maxdepth 3 -printf '%y %p -> %l\n'
run find /generation-evidence -maxdepth 4 -printf '%y %p -> %l\n'
run sha256sum /audit-input.json /audit-campaign-lock.json
run jq . /audit-input.json
run jq . /audit-campaign-lock.json
run jq . /run.json
run jq . /task.json
run jq . /generation-result.json
run jq . /generation-evidence/invocation.json
run jq . /generation-evidence/metrics.json
run jq . /generation-evidence/runtime-metrics.json
run jq . /generation-evidence/usage.json
run sed -n 1,240p /generation-evidence/codex-last.txt
run sed -n 1,320p /generation-evidence/codex-output.log
run sed -n 1,320p /generation-evidence/prompt.txt

exit "$status"
