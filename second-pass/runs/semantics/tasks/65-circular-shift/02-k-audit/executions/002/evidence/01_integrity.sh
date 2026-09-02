#!/usr/bin/env bash
set -uo pipefail

echo '$ python3 /audit-output/evidence/01_integrity_check.py'
python3 /audit-output/evidence/01_integrity_check.py
status=$?
echo "EXIT_STATUS=$status"

echo '$ cmp /candidate/reference-semantics /reference/reference-semantics via recursive diff'
diff --recursive --no-dereference --brief \
  /candidate/reference-semantics \
  /reference/reference-semantics
diff_status=$?
echo "EXIT_STATUS=$diff_status"

echo '$ find required mounts for symlinks and special entries'
find /candidate /reference /generation-evidence \
  \( -type l -o \( ! -type f ! -type d \) \) \
  -printf '%y %m %p -> %l\n'
find_status=$?
echo "EXIT_STATUS=$find_status"

if (( status != 0 || diff_status != 0 || find_status != 0 )); then
  exit 1
fi
