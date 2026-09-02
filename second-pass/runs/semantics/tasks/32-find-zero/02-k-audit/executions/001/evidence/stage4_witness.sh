#!/usr/bin/env bash
set +e

printf 'COMMAND: python3 /audit-output/evidence/entry_witness.py\n'
python3 /audit-output/evidence/entry_witness.py
printf 'EXIT_STATUS: %d\n' "$?"
