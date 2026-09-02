#!/usr/bin/env bash
set -u

work=/tmp/audit-work/37-sort-even-audit/reconstruction-fresh
evidence=/audit-output/evidence
status=0

echo '$ python3 /audit-output/evidence/ground_witness.py'
python3 "$evidence/ground_witness.py"
python_status=$?
echo "exit=$python_status"
status=$((status | python_status))

echo '$ cd /tmp/audit-work/37-sort-even-audit/reconstruction-fresh'
cd "$work" || exit 1
echo "exit=$?"

echo '$ kprove /audit-output/evidence/spec-ground.k --definition verification-kompiled --spec-module GROUND-SPEC --claims SPEC.loop-correct,GROUND-SPEC.ground-example --trusted SPEC.loop-correct --output pretty'
kprove "$evidence/spec-ground.k" \
  --definition verification-kompiled \
  --spec-module GROUND-SPEC \
  --claims SPEC.loop-correct,GROUND-SPEC.ground-example \
  --trusted SPEC.loop-correct \
  --output pretty
proof_status=$?
echo "exit=$proof_status"
status=$((status | proof_status))

echo "stage4_exit=$status"
exit "$status"
