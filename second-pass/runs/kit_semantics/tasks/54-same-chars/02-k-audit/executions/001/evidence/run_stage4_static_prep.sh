#!/usr/bin/env bash
set -euo pipefail
set -o xtrace
python3 /audit-output/evidence/k_rule_inventory.py > /audit-output/evidence/rule_inventory.tsv
python3 /audit-output/evidence/k_rule_inventory.py --summary
python3 /audit-output/evidence/ground_substitution_check.py
printf 'EXIT_STATUS=0\n'
