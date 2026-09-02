#!/usr/bin/env bash
set -u

echo "command: python3 /audit-output/evidence/provenance_claims.py"
python3 /audit-output/evidence/provenance_claims.py
rc=$?
echo "exit: $rc"
echo "script_exit: $rc"
exit "$rc"
