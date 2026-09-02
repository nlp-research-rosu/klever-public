#!/usr/bin/env bash
set -u

run_logged() {
  local label="$1"
  shift
  local log="/audit-output/evidence/${label}.log"
  {
    printf 'CWD: %s\n' "$PWD"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    local status=$?
    printf 'EXIT_STATUS: %d\n' "$status"
    return "$status"
  } >"$log" 2>&1
}

cd /audit-output || exit 90
run_logged 01-provenance python3 /audit-output/evidence/provenance_check.py
provenance_status=$?

cd /tmp/audit-work/68-pluck || exit 91
run_logged 02-translate bash -c \
  'python3 py2mpy.py solution.py > regenerated-solution.mpy && cmp -s regenerated-solution.mpy solution.mpy && sha256sum regenerated-solution.mpy solution.mpy'
translation_status=$?
run_logged 03-differential python3 /audit-output/evidence/differential_test.py
differential_status=$?

printf 'provenance=%d translation=%d differential=%d\n' \
  "$provenance_status" "$translation_status" "$differential_status"
if (( provenance_status != 0 || translation_status != 0 || differential_status != 0 )); then
  exit 1
fi
