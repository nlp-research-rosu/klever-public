#!/usr/bin/env bash
set -uo pipefail

record_status() {
  local label="$1"
  local status="$2"
  printf 'STATUS [%s]: %s\n' "$label" "$status"
  if [[ "$status" -ne 0 ]]; then
    exit "$status"
  fi
}

printf '%s\n' \
  'COMMAND: python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/solution.regenerated.mpy'
python3 /reference/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
status=$?
record_status "trusted regeneration" "$status"

printf '%s\n' \
  'COMMAND: cmp /tmp/audit-work/reconstruction/solution.regenerated.mpy /tmp/audit-work/reconstruction/solution.mpy'
cmp \
  /tmp/audit-work/reconstruction/solution.regenerated.mpy \
  /tmp/audit-work/reconstruction/solution.mpy
status=$?
record_status "solution.mpy byte identity" "$status"

printf '%s\n' \
  'COMMAND: sha256sum /tmp/audit-work/reconstruction/solution.regenerated.mpy /tmp/audit-work/reconstruction/solution.mpy'
sha256sum \
  /tmp/audit-work/reconstruction/solution.regenerated.mpy \
  /tmp/audit-work/reconstruction/solution.mpy
status=$?
record_status "translation hashes" "$status"

printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/02_differential_test.py'
python3 /audit-output/evidence/02_differential_test.py
status=$?
record_status "differential test" "$status"

printf '%s\n' 'RESULT: fidelity checks passed'
