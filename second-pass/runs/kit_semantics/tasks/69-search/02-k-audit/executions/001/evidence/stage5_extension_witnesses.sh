#!/usr/bin/env bash
set -uo pipefail
set -x

cd /tmp/audit-work/reconstruction
status=0
cp /audit-output/evidence/extension_ground.k extension_ground.k
cp /audit-output/evidence/extension_false.k extension_false.k

kprove extension_ground.k \
  --definition audit-verification-kompiled \
  --spec-module EXTENSION-GROUND \
  2>&1 |
  tail -n 200 |
  tee /audit-output/evidence/stage5_extension_ground_bounded.log
ground_exit="${PIPESTATUS[0]}"
printf 'ground_claims_exit=%s\n' "$ground_exit"
if [[ "$ground_exit" != 0 ]] ||
   ! grep -qx '#Top' /audit-output/evidence/stage5_extension_ground_bounded.log; then
  status=1
fi

for label in wrong-project wrong-addition wrong-summary; do
  kprove extension_false.k \
    --definition audit-verification-kompiled \
    --spec-module EXTENSION-FALSE \
    --claims "EXTENSION-FALSE.$label" \
    2>&1 |
    tail -n 200 |
    tee "/audit-output/evidence/stage5_${label}_bounded.log"
  false_exit="${PIPESTATUS[0]}"
  printf 'false_claim=%s exit=%s\n' "$label" "$false_exit"
  if [[ "$false_exit" == 0 ]] ||
     grep -qx '#Top' "/audit-output/evidence/stage5_${label}_bounded.log" ||
     ! grep -q 'WarnStuckClaimState' "/audit-output/evidence/stage5_${label}_bounded.log"; then
    status=1
  fi
done

printf 'stage5_extension_witnesses_exit=%s\n' "$status"
exit "$status"
