#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/145-order-by-points-002
evidence=/audit-output/evidence
overall=0

echo "$ python3 $evidence/adequacy_witnesses.py"
python3 "$evidence/adequacy_witnesses.py"
command_status=$?
echo "EXIT (Python witnesses): $command_status"
if [ "$command_status" -ne 0 ]; then overall=1; fi

echo "$ cp $evidence/body_sensitivity.k $scratch/audit-body-sensitivity.k"
cp "$evidence/body_sensitivity.k" "$scratch/audit-body-sensitivity.k"
command_status=$?
echo "EXIT (copy reviewer mutation to scratch): $command_status"
if [ "$command_status" -ne 0 ]; then overall=1; fi

echo "$ cd $scratch"
cd "$scratch" || exit 1
echo "EXIT: 0"

echo "$ timeout --signal=TERM 120s kprove audit-body-sensitivity.k --definition audit-verification-kompiled --spec-module AUDIT-BODY-SENSITIVITY --claims AUDIT-BODY-SENSITIVITY.changed-executed-helper-body"
timeout --signal=TERM 120s \
  kprove audit-body-sensitivity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-BODY-SENSITIVITY \
  --claims AUDIT-BODY-SENSITIVITY.changed-executed-helper-body \
  > "$evidence/stage4_body_sensitivity_proof.log" 2>&1
proof_status=$?
echo "EXIT (expected nonzero): $proof_status"
sed -n '1,220p' "$evidence/stage4_body_sensitivity_proof.log"
if [ "$proof_status" -eq 0 ]; then
  echo "UNEXPECTED body-sensitivity proof success"
  overall=1
fi
if [ "$proof_status" -eq 124 ]; then
  echo "UNEXPECTED body-sensitivity timeout"
  overall=1
fi
if ! rg -q 'WarnStuckClaimState' \
    "$evidence/stage4_body_sensitivity_proof.log"; then
  echo "MISSING expected stuck-claim residual"
  overall=1
fi
if ! rg -q '#Equals|0' "$evidence/stage4_body_sensitivity_proof.log"; then
  echo "MISSING expected changed-result evidence"
  overall=1
fi

echo "STAGE4 SCRIPT EXIT: $overall"
exit "$overall"
