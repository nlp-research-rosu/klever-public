#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/candidate-clean
evidence=/audit-output/evidence

echo 'AUDIT COMMAND: bash /audit-output/evidence/stage4_adequacy.sh'
echo 'COMMAND: python3 /audit-output/evidence/build_stage4_specs.py'
python3 "$evidence/build_stage4_specs.py" \
  | tee "$evidence/stage4_ground_witnesses.log"

echo 'COMMAND: kprove ast-identity.k --definition verification-audit-kompiled --spec-module AST-IDENTITY'
set +e
(
  cd "$work"
  kprove \
    ast-identity.k \
    --definition verification-audit-kompiled \
    --spec-module AST-IDENTITY
) 2>&1 | tee "$evidence/stage4_ast_identity.log"
status=${PIPESTATUS[0]}
set -e
echo "ast_identity_exit=$status"
top_count="$(grep -xc '#Top' "$evidence/stage4_ast_identity.log" || true)"
echo "ast_identity_top_count=$top_count"
test "$status" -eq 0
test "$top_count" -eq 1

echo 'COMMAND: kprove adequacy-ground.k --definition verification-audit-kompiled --spec-module ADEQUACY-GROUND'
set +e
(
  cd "$work"
  kprove \
    adequacy-ground.k \
    --definition verification-audit-kompiled \
    --spec-module ADEQUACY-GROUND
) 2>&1 | tee "$evidence/stage4_ground_summaries.log"
status=${PIPESTATUS[0]}
set -e
echo "ground_summaries_exit=$status"
top_count="$(grep -xc '#Top' "$evidence/stage4_ground_summaries.log" || true)"
echo "ground_summaries_top_count=$top_count"
test "$status" -eq 0
test "$top_count" -eq 1

sha256sum \
  "$work/ast-identity.k" \
  "$work/adequacy-ground.k" \
  "$work/solution.mpy"
echo 'STAGE4_ADEQUACY_EXIT=0'
