#!/usr/bin/env bash
set -eu
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT_STATUS=%s\n" "$status"' EXIT
set -x

cd /tmp/audit-work/108-count-nums-clean-rebuild
krun solution.mpy --definition semantic-kompiled -cARG='list(-10)' \
  | grep -F 'IntV ( 0 ) ~> .K'
test "${PIPESTATUS[0]}" -eq 0
krun solution.mpy --definition semantic-kompiled -cARG='list(-9)' \
  | grep -F 'IntV ( 0 ) ~> .K'
test "${PIPESTATUS[0]}" -eq 0
krun solution.mpy --definition semantic-kompiled -cARG='list(9)' \
  | grep -F 'IntV ( 1 ) ~> .K'
test "${PIPESTATUS[0]}" -eq 0
krun solution.mpy --definition semantic-kompiled -cARG='list(10)' \
  | grep -F 'IntV ( 1 ) ~> .K'
test "${PIPESTATUS[0]}" -eq 0
