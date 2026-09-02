#!/usr/bin/env bash
set -u

cd /tmp/audit-work/review-59/candidate-src || exit 90

echo '$ kprove ground-instances.k --definition verification-kompiled --spec-module GROUND-INSTANCES'
kprove ground-instances.k \
  --definition verification-kompiled \
  --spec-module GROUND-INSTANCES
proof_status=$?
echo "exit=$proof_status"

echo '$ python3 /audit-output/evidence/ground_comparison.py'
python3 /audit-output/evidence/ground_comparison.py
comparison_status=$?
echo "exit=$comparison_status"

if [ "$proof_status" -ne 0 ] || [ "$comparison_status" -ne 0 ]; then
  exit 1
fi
