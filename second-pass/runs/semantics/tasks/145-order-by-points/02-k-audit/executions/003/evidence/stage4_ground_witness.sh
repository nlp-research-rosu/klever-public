#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/ground_claim_witness.py'
python3 /audit-output/evidence/ground_claim_witness.py
printf 'EXIT_STATUS: %s\n' "$?"
