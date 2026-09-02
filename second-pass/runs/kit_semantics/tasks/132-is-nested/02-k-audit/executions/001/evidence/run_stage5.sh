#!/usr/bin/env bash
set -uo pipefail

echo '$ python3 /audit-output/evidence/k_rule_inventory.py > /audit-output/evidence/k_rule_inventory.md'
python3 /audit-output/evidence/k_rule_inventory.py \
  > /audit-output/evidence/k_rule_inventory.md
inventory_status=$?
echo "EXIT_STATUS: ${inventory_status}"

echo '$ rg -n "\\[(functional|simplification|priority|concrete|owise)|no-evaluators|\\btotal\\b|\\bfunction\\b" /reference/reference-semantics /candidate/verification.k /candidate/spec.k'
rg -n '\[(functional|simplification|priority|concrete|owise)|no-evaluators|\btotal\b|\bfunction\b' \
  /reference/reference-semantics /candidate/verification.k /candidate/spec.k
rg_status=$?
echo "EXIT_STATUS: ${rg_status}"

echo '$ rg -n "simplification|functional" /reference/reference-semantics /candidate/verification.k /candidate/spec.k'
rg -n 'simplification|functional' \
  /reference/reference-semantics /candidate/verification.k /candidate/spec.k
absence_status=$?
echo "EXIT_STATUS: ${absence_status} (1 means no matches, as expected)"

echo '$ sed -n "1,80p" /audit-output/evidence/k_rule_inventory.md'
sed -n '1,80p' /audit-output/evidence/k_rule_inventory.md
head_status=$?
echo "EXIT_STATUS: ${head_status}"

echo '$ wc -l -c /audit-output/evidence/k_rule_inventory.md /audit-output/evidence/used_construct_map.md'
wc -l -c /audit-output/evidence/k_rule_inventory.md \
  /audit-output/evidence/used_construct_map.md
wc_status=$?
echo "EXIT_STATUS: ${wc_status}"
