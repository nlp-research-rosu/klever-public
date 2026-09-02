#!/usr/bin/env bash
set -u

echo '$ python3 /audit-output/evidence/generation_claims_digest.py'
python3 /audit-output/evidence/generation_claims_digest.py
digest_status=$?
echo "EXIT_STATUS=$digest_status"
exit "$digest_status"
