#!/usr/bin/env bash
set +e
work=/tmp/audit-work/candidate-src

cp /audit-output/evidence/false-result-spec.k "$work/false-result-spec.k"

echo '$ kprove /tmp/audit-work/candidate-src/false-result-spec.k --definition /tmp/audit-work/verification-kompiled --spec-module FALSE-RESULT-SPEC --dry-run'
kprove "$work/false-result-spec.k" \
  --definition /tmp/audit-work/verification-kompiled \
  --spec-module FALSE-RESULT-SPEC \
  --dry-run
build_status=$?
echo "FALSE_MUTATION_DRY_RUN_EXIT_STATUS=$build_status"

echo '$ kprove /tmp/audit-work/candidate-src/false-result-spec.k --definition /tmp/audit-work/verification-kompiled --spec-module FALSE-RESULT-SPEC'
kprove "$work/false-result-spec.k" \
  --definition /tmp/audit-work/verification-kompiled \
  --spec-module FALSE-RESULT-SPEC
proof_status=$?
echo "FALSE_MUTATION_KPROVE_EXIT_STATUS=$proof_status"

if (( build_status != 0 )); then
  echo 'NONVACUITY_RESULT=INVALID_MUTATION_BUILD'
  exit 1
fi
if (( proof_status == 0 )); then
  echo 'NONVACUITY_RESULT=UNEXPECTED_PROOF'
  exit 1
fi
echo 'NONVACUITY_RESULT=EXPECTED_UNMET_RESULT_OBLIGATION'
exit 0
