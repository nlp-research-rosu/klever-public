#!/usr/bin/env bash
set -u

echo '$ python3 concrete_semantics_test.py --work /tmp/audit-work/final-reconstruction --definition /tmp/audit-work/final-reconstruction/semantic-audit-kompiled'
python3 /audit-output/evidence/concrete_semantics_test.py \
  --work /tmp/audit-work/final-reconstruction \
  --definition /tmp/audit-work/final-reconstruction/semantic-audit-kompiled
status=$?
echo "EXIT_STATUS=$status"
exit "$status"
