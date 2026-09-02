#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/vacuity
definition="$work/vacuity-verification-kompiled"
raw=/audit-output/evidence/nonvacuity_kprove.raw.log

echo 'MUTATION: swap the two components of the end-to-end result obligation'
echo 'SATISFYING_WITNESS: IS=icon(-2,icon(3,nil)), env=.Map, steps=0'
echo 'TRUE_RESULT_FOR_WITNESS: pyTuple(pyInt(-2),pyInt(3))'
echo 'MUTATED_REQUIRED_RESULT: pyTuple(pyInt(3),pyInt(-2))'
echo 'COMMAND: diff -u reconstruction/spec.k vacuity/spec-vacuity.k'
diff -u \
  /tmp/audit-work/reconstruction/spec.k \
  "$work/spec-vacuity.k"
diff_status=$?
echo "DIFF_EXIT_STATUS=$diff_status (1 means the intended mutation is present)"

echo 'COMMAND: timeout 900 kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition vacuity-verification-kompiled'
(
  cd "$work" || exit 98
  timeout 900 kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition "$definition"
)
build_status=$?
echo "DEFINITION_BUILD_EXIT_STATUS=$build_status"
if (( build_status != 0 )); then
  exit 1
fi

echo 'COMMAND: timeout 300 kprove spec-vacuity.k --definition vacuity-verification-kompiled --spec-module SPEC-VACUITY --dry-run'
(
  cd "$work" || exit 98
  timeout 300 kprove spec-vacuity.k \
    --definition "$definition" \
    --spec-module SPEC-VACUITY \
    --dry-run
)
dry_status=$?
echo "MUTATED_SPEC_BUILD_EXIT_STATUS=$dry_status"
if (( dry_status != 0 )); then
  exit 1
fi

echo 'COMMAND: timeout 900 kprove spec-vacuity.k --definition vacuity-verification-kompiled --spec-module SPEC-VACUITY'
(
  cd "$work" || exit 98
  timeout 900 kprove spec-vacuity.k \
    --definition "$definition" \
    --spec-module SPEC-VACUITY
) 2>&1 | tee "$raw"
prove_status=${PIPESTATUS[0]}
echo "MUTATED_PROOF_EXIT_STATUS=$prove_status"

if (( prove_status == 0 )); then
  echo 'NONVACUITY=FAIL (false result obligation proved)'
  exit 1
fi
if ! grep -q 'WarnStuckClaimState' "$raw"; then
  echo 'NONVACUITY=FAIL (failure was not a stuck proof obligation)'
  exit 1
fi
if grep -Eq 'Parser|parse error|Could not find|does not exist' "$raw"; then
  echo 'NONVACUITY=FAIL (failure included a build/parser error)'
  exit 1
fi
echo 'NONVACUITY=PASS (false result obligation was rejected as stuck)'
exit 0
