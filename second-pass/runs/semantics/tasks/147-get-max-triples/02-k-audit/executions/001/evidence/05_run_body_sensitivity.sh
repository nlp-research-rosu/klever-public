#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
definition="$work/audit-body-mutated-kompiled"
cd "$work" || exit 125

echo 'MUTATION: submitted return value changed to zero_triples + one_triples + 1; postcondition left unchanged'

echo 'COMMAND: kompile /audit-output/evidence/05_verification_body_mutated.k --backend haskell --main-module AUDIT-BODY-MUTATED --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/reconstruction/audit-body-mutated-kompiled -I /tmp/audit-work/reconstruction'
kompile /audit-output/evidence/05_verification_body_mutated.k \
  --backend haskell \
  --main-module AUDIT-BODY-MUTATED \
  --syntax-module MPY-SYNTAX \
  --output-definition "$definition" \
  -I "$work"
build_status=$?
echo "EXIT_STATUS: $build_status"

echo 'COMMAND: kprove /audit-output/evidence/05_body_mutation_spec.k --definition /tmp/audit-work/reconstruction/audit-body-mutated-kompiled --spec-module AUDIT-BODY-MUTATION-SPEC --claims AUDIT-BODY-MUTATION-SPEC.unchanged-postcondition -I /audit-output/evidence -I /tmp/audit-work/reconstruction --output pretty'
kprove /audit-output/evidence/05_body_mutation_spec.k \
  --definition "$definition" \
  --spec-module AUDIT-BODY-MUTATION-SPEC \
  --claims AUDIT-BODY-MUTATION-SPEC.unchanged-postcondition \
  -I /audit-output/evidence \
  -I "$work" \
  --output pretty
proof_status=$?
echo "EXIT_STATUS: $proof_status"

if (( build_status == 0 && proof_status != 0 )); then
  echo 'BODY_SENSITIVITY_EXPECTATION_MET'
  exit 0
fi
echo 'BODY_SENSITIVITY_EXPECTATION_NOT_MET'
exit 1
