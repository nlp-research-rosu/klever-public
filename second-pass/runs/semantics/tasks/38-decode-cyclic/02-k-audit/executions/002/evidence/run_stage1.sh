#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage1_integrity.log
{
  echo '$ python3 /audit-output/evidence/stage1_integrity.py'
  python3 /audit-output/evidence/stage1_integrity.py
  status=$?
  echo "EXIT_STATUS=$status"
  exit "$status"
} >"$log" 2>&1
