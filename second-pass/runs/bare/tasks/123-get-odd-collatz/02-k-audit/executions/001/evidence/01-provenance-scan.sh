#!/usr/bin/env bash
set -o pipefail

echo 'COMMAND: python3 /audit-output/evidence/01-provenance-scan.py'
python3 /audit-output/evidence/01-provenance-scan.py
rc=$?
echo "EXIT: $rc"
exit "$rc"
