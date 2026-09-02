#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/body-mutation
definition="$work/body-mutation-kompiled"
raw=/audit-output/evidence/body_mutation_kprove.raw.log

echo 'MUTATION: solutionProgram returns (smallest_positive, largest_negative)'
echo 'COMMAND: diff -u reconstruction/verification.k body-mutation/verification.k'
diff -u \
  /tmp/audit-work/reconstruction/verification.k \
  "$work/verification.k"
diff_status=$?
echo "DIFF_EXIT_STATUS=$diff_status (1 means the intended mutation is present)"

echo 'COMMAND: timeout 900 kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutation-kompiled'
(
  cd "$work" || exit 98
  timeout 900 kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition "$definition"
)
build_status=$?
echo "BUILD_EXIT_STATUS=$build_status"
if (( build_status != 0 )); then
  exit 1
fi

echo 'COMMAND: timeout 900 kprove spec.k --definition body-mutation-kompiled --spec-module SPEC'
(
  cd "$work" || exit 98
  timeout 900 kprove spec.k \
    --definition "$definition" \
    --spec-module SPEC
) 2>&1 | tee "$raw"
prove_status=${PIPESTATUS[0]}
echo "PROOF_EXIT_STATUS=$prove_status"

if (( prove_status == 0 )); then
  echo 'BODY_SENSITIVITY=FAIL (mutated body still proved)'
  exit 1
fi
if ! grep -q 'WarnStuckClaimState' "$raw"; then
  echo 'BODY_SENSITIVITY=FAIL (failure was not a stuck proof obligation)'
  exit 1
fi
echo 'BODY_SENSITIVITY=PASS (mutated executed constructor term was rejected)'
exit 0
