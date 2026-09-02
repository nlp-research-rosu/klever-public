#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/candidate-clean
evidence=/audit-output/evidence

echo 'AUDIT COMMAND: bash /audit-output/evidence/stage5_body_sensitivity.sh'
echo 'COMMAND: python3 /audit-output/evidence/build_body_mutation.py'
python3 "$evidence/build_body_mutation.py"

echo 'COMMAND: kompile --backend haskell verification-body-mutated.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-body-mutated-kompiled'
set +e
(
  cd "$work"
  kompile \
    --backend haskell \
    verification-body-mutated.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-body-mutated-kompiled
) 2>&1 | tee "$evidence/stage5_body_mutation_kompile.log"
status=${PIPESTATUS[0]}
set -e
echo "body_mutation_kompile_exit=$status"
test "$status" -eq 0

echo 'COMMAND: kprove body-mutation-ground.k --definition verification-body-mutated-kompiled --spec-module BODY-MUTATION-GROUND'
set +e
(
  cd "$work"
  kprove \
    body-mutation-ground.k \
    --definition verification-body-mutated-kompiled \
    --spec-module BODY-MUTATION-GROUND
) 2>&1 | tee "$evidence/stage5_body_mutation_kprove.log"
status=${PIPESTATUS[0]}
set -e
echo "body_mutation_kprove_exit=$status"
test "$status" -ne 0
grep -q 'WarnStuckClaimState' "$evidence/stage5_body_mutation_kprove.log"
grep -q 'str ( .IntSeq )' "$evidence/stage5_body_mutation_kprove.log"
echo 'body_mutation_expected_unmet_result=true'
echo 'STAGE5_BODY_SENSITIVITY_EXIT=0'
