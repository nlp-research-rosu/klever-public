#!/usr/bin/env bash
set -u
printf '$ python3 /audit-output/evidence/claim_witnesses.py\n'
python3 /audit-output/evidence/claim_witnesses.py
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
