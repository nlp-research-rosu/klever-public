#!/usr/bin/env bash
set -o pipefail

echo 'COMMAND: python3 /audit-output/evidence/04-adequacy-pinning.py'
python3 /audit-output/evidence/04-adequacy-pinning.py
rc=$?
echo "EXIT: $rc"
exit "$rc"
