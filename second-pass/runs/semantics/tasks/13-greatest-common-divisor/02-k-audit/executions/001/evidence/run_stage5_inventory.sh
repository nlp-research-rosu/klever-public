#!/usr/bin/env bash
set +e

printf 'COMMAND: python3 /audit-output/evidence/build_rule_inventory.py\n'
python3 /audit-output/evidence/build_rule_inventory.py
status=$?
printf 'EXIT STATUS: %d\n' "$status"
exit "$status"
