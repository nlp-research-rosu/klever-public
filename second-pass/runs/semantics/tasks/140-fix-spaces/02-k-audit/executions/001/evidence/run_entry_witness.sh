#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/entry_claim_witness.py\n'
python3 /audit-output/evidence/entry_claim_witness.py
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
