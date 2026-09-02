#!/usr/bin/env bash
set -u

evidence=/audit-output/evidence
overall=0

{
  echo "COMMAND: kprove mutated spec --dry-run"
  kprove spec-vacuity-review.k \
    --definition reviewer-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.main-correct,SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
    --trusted SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
    --dry-run \
    --output pretty
  dry_rc=$?
  echo "EXIT_STATUS=$dry_rc"
} > "$evidence/06-vacuity-dry-run.log" 2>&1
echo "dry_run_exit=$dry_rc"
(( dry_rc == 0 )) || overall=1

{
  echo "COMMAND: kprove result+1 mutated spec"
  kprove spec-vacuity-review.k \
    --definition reviewer-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.main-correct,SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
    --trusted SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
    --output pretty
  proof_rc=$?
  echo "EXIT_STATUS=$proof_rc"
} > "$evidence/06-vacuity-proof.log" 2>&1
echo "mutated_proof_exit=$proof_rc"
if (( proof_rc == 0 )); then
  overall=1
elif rg -q 'WarnStuckClaimState' "$evidence/06-vacuity-proof.log" \
  && rg -q 'implication check between the conditions has failed' \
    "$evidence/06-vacuity-proof.log" \
  && rg -q 'digitAcc.*\+Int 1|\+Int 1' \
    "$evidence/06-vacuity-proof.log"; then
  echo "expected unmet result obligation observed"
else
  overall=1
fi

{
  echo "COMMAND: concrete satisfying witness [2]"
  python3 -c '
from solution import skjkasdkd
actual = skjkasdkd([2])
print("input=[2] actual=", actual, "mutated_target=", actual + 1)
assert actual == 2
'
  witness_rc=$?
  echo "EXIT_STATUS=$witness_rc"
} > "$evidence/06-vacuity-witness.log" 2>&1
echo "witness_exit=$witness_rc"
(( witness_rc == 0 )) || overall=1

echo "FINAL_STATUS=$overall"
exit "$overall"
