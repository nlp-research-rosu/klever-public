#!/usr/bin/env bash
set -u

printf 'Audit stage 4: claim adequacy and real-program pinning\n'
printf '\n$ python3 /audit-output/evidence/claim_adequacy.py\n'
python3 /audit-output/evidence/claim_adequacy.py
status=$?
printf '[exit_status] %d\n' "$status"
exit "$status"
