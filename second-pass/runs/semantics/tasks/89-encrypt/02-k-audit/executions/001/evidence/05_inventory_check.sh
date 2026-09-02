#!/usr/bin/env bash
set -u

echo 'COMMAND: python3 /audit-output/evidence/rule_inventory.py > /tmp/audit-work/rule_inventory.check.md'
python3 /audit-output/evidence/rule_inventory.py \
  > /tmp/audit-work/rule_inventory.check.md
audit_generate_status=$?
echo "EXIT_STATUS: ${audit_generate_status}"

echo 'COMMAND: cmp -s /tmp/audit-work/rule_inventory.check.md /audit-output/evidence/05_rule_inventory.md'
cmp -s /tmp/audit-work/rule_inventory.check.md \
  /audit-output/evidence/05_rule_inventory.md
audit_identity_status=$?
echo "EXIT_STATUS: ${audit_identity_status}"

echo 'COMMAND: rg inventory summary fields'
rg -n \
  'Total inventoried|^- (claim|configuration|context|rule|syntax):|No \\[simplification\\]|no-evaluators|operational bridge' \
  /audit-output/evidence/05_rule_inventory.md \
  /audit-output/evidence/05_used_constructs.md
audit_summary_status=$?
echo "EXIT_STATUS: ${audit_summary_status}"

if (( audit_generate_status != 0 || audit_identity_status != 0 || audit_summary_status != 0 )); then
  exit 1
fi
