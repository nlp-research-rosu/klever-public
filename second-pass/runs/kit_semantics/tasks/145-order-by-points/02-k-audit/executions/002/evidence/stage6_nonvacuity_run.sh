#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/145-order-by-points-002
evidence=/audit-output/evidence
overall=0

echo "SATISFYING WITNESS input=[1,11,-1,-11,-12]"
echo "CORRECT result=[-1,-11,1,-12,11]"
echo "FALSE MUTATION result=[11,-12,1,-11,-1]"

echo "$ cp $evidence/fresh_nonvacuity.k $scratch/audit-fresh-nonvacuity.k"
cp "$evidence/fresh_nonvacuity.k" "$scratch/audit-fresh-nonvacuity.k"
copy_status=$?
echo "EXIT (copy reviewer mutation to scratch): $copy_status"
if [ "$copy_status" -ne 0 ]; then overall=1; fi

echo "$ cd $scratch"
cd "$scratch" || exit 1
echo "EXIT: 0"

echo "$ timeout --signal=TERM 120s kprove audit-fresh-nonvacuity.k --definition audit-verification-kompiled --spec-module AUDIT-NONVACUITY --claims AUDIT-NONVACUITY.reversed-target-result --dry-run"
timeout --signal=TERM 120s \
  kprove audit-fresh-nonvacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-NONVACUITY \
  --claims AUDIT-NONVACUITY.reversed-target-result \
  --dry-run \
  > "$evidence/stage6_mutation_build.log" 2>&1
build_status=$?
echo "EXIT (mutation build): $build_status"
sed -n '1,180p' "$evidence/stage6_mutation_build.log"
if [ "$build_status" -ne 0 ]; then overall=1; fi

echo "$ timeout --signal=TERM 120s kprove audit-fresh-nonvacuity.k --definition audit-verification-kompiled --spec-module AUDIT-NONVACUITY --claims AUDIT-NONVACUITY.reversed-target-result"
timeout --signal=TERM 120s \
  kprove audit-fresh-nonvacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-NONVACUITY \
  --claims AUDIT-NONVACUITY.reversed-target-result \
  > "$evidence/stage6_mutation_proof.log" 2>&1
proof_status=$?
echo "EXIT (expected nonzero proof): $proof_status"
sed -n '1,240p' "$evidence/stage6_mutation_proof.log"
if [ "$proof_status" -eq 0 ]; then
  echo "UNEXPECTED mutation proof success"
  overall=1
fi
if [ "$proof_status" -eq 124 ]; then
  echo "UNEXPECTED mutation proof timeout"
  overall=1
fi
if ! rg -q 'WarnStuckClaimState' "$evidence/stage6_mutation_proof.log"; then
  echo "MISSING expected stuck-claim residual"
  overall=1
fi
if ! rg -q 'revVS|sortKeyVS|expectedOrder' \
    "$evidence/stage6_mutation_proof.log"; then
  echo "MISSING expected reversed-result residual"
  overall=1
fi

echo "STAGE6 SCRIPT EXIT: $overall"
exit "$overall"
