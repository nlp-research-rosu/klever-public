#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/structural-audit.log

{
  printf '%s\n' '$ env PYTHONPATH=/reference python3 /audit-output/evidence/structural_audit.py'
  env PYTHONPATH=/reference python3 /audit-output/evidence/structural_audit.py
  code=$?
  printf '\nEXIT_CODE: %s\n' "$code"
  exit "$code"
} >"$log" 2>&1
