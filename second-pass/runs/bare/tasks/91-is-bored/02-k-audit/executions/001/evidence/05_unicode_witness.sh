#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/unicode_semantics_witness.py'
python3 /audit-output/evidence/unicode_semantics_witness.py
code=$?
printf 'EXIT: %s\n' "$code"
# The nonzero result is the expected audit finding, not a driver failure.
exit 0
