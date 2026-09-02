#!/usr/bin/env bash
set -u

echo '$ python3 /audit-output/evidence/k_inventory.py'
python3 /audit-output/evidence/k_inventory.py
status=$?
echo "EXIT: $status"
echo '$ rg -n "^[[:space:]]*(configuration|syntax|context|rule|claim)\\b" /tmp/audit-work/fresh/reference-semantics /tmp/audit-work/fresh/verification.k /tmp/audit-work/fresh/spec.k'
rg -n '^[[:space:]]*(configuration|syntax|context|rule|claim)\b' \
  /tmp/audit-work/fresh/reference-semantics \
  /tmp/audit-work/fresh/verification.k \
  /tmp/audit-work/fresh/spec.k
rg_status=$?
echo "EXIT: $rg_status"
exit "$status"
