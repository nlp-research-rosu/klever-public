#!/usr/bin/env bash
set +e

echo '$ python3 /audit-output/evidence/provenance_inspect.py'
python3 /audit-output/evidence/provenance_inspect.py
status=$?
echo "EXIT_STATUS=$status"
exit "$status"
