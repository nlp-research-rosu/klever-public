#!/usr/bin/env bash
set -u

record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status"
  return "$status"
}

overall=0
work=/tmp/audit-work/124-valid-date

record bash -c \
  'sed "s/\\.Stmts//g" /tmp/audit-work/124-valid-date/embedded-solution.mpy > /tmp/audit-work/124-valid-date/embedded-solution.concrete.mpy' \
  || overall=1

printf 'COMMAND: kast %q --definition %q --input program --output json > %q\n' \
  "$work/embedded-solution.concrete.mpy" \
  "$work/runtime-fresh-kompiled" \
  "$work/embedded-solution.concrete.kast.json"
kast "$work/embedded-solution.concrete.mpy" \
  --definition "$work/runtime-fresh-kompiled" \
  --input program \
  --output json > "$work/embedded-solution.concrete.kast.json"
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
if (( status != 0 )); then overall=1; fi

record cmp \
  "$work/solution.kast.json" \
  "$work/embedded-solution.concrete.kast.json" \
  || overall=1
record sha256sum \
  "$work/solution.kast.json" \
  "$work/embedded-solution.concrete.kast.json" \
  || overall=1

printf 'OVERALL_STATUS: %d\n' "$overall"
exit "$overall"
