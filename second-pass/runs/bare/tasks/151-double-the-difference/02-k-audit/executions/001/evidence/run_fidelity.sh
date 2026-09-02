#!/usr/bin/env bash
set -u

record_status() {
  local label="$1"
  local status="$2"
  printf '%s_EXIT_STATUS=%s\n' "$label" "$status"
  if [[ "$status" -ne 0 ]]; then
    exit "$status"
  fi
}

printf '%s\n' \
  'COMMAND: python3 /tmp/audit-work/reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/regenerated-solution.mpy'
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
status=$?
record_status TRANSLATOR "$status"

printf '%s\n' \
  'COMMAND: cmp /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate-src/solution.mpy'
cmp /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
status=$?
record_status BYTE_IDENTITY "$status"

printf '%s\n' \
  'COMMAND: sha256sum /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate-src/solution.mpy'
sha256sum /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
status=$?
record_status SHA256 "$status"

printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
status=$?
record_status DIFFERENTIAL "$status"
