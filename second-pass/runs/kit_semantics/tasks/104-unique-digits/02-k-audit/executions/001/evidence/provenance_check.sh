#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

run python3 /audit-output/evidence/provenance_check.py
run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py
run diff --no-dereference --recursive /candidate/reference-semantics /reference/reference-semantics

printf '$ find /candidate /reference /generation-evidence -xdev -type l -print\n'
find /candidate /reference /generation-evidence -xdev -type l -print
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
test "$status" -eq 0

for mounted in \
  /candidate \
  /generation-evidence \
  /run.json \
  /task.json \
  /generation-result.json \
  /audit-input.json \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/reference-semantics
do
  run findmnt -T "$mounted" -n -o TARGET,OPTIONS
done
