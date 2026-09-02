#!/usr/bin/env bash
set +e

printf 'COMMAND: python3 /audit-output/evidence/stage4_witnesses.py\n'
python3 /audit-output/evidence/stage4_witnesses.py
status=$?
printf 'EXIT STATUS: %d\n' "$status"
exit "$status"
