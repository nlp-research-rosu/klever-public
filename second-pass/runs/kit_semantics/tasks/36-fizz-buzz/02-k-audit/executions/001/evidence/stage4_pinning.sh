#!/usr/bin/env bash
set +e

printf 'COMMAND: python3 /audit-output/evidence/constructor_identity.py\n'
python3 /audit-output/evidence/constructor_identity.py
status=$?
printf 'EXIT STATUS: %s\n' "$status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

printf 'COMMAND: python3 /audit-output/evidence/claim_witnesses.py\n'
python3 /audit-output/evidence/claim_witnesses.py
status=$?
printf 'EXIT STATUS: %s\n' "$status"
exit "$status"
