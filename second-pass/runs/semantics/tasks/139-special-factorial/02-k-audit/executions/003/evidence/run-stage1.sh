#!/usr/bin/env bash
set -o pipefail
set -x

jq . /audit-input.json
jq . /audit-campaign-lock.json
find /candidate /reference /generation-evidence -maxdepth 3 -printf '%y %p -> %l\n' | sort
stat -c '%F %s %n' \
  /run.json \
  /task.json \
  /generation-result.json \
  /audit-input.json \
  /audit-campaign-lock.json
