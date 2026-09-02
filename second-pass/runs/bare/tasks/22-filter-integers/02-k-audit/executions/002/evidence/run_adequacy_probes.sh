#!/usr/bin/env bash
set +e

echo '$ python3 /audit-output/evidence/pinning_check.py'
python3 /audit-output/evidence/pinning_check.py
pin_status=$?
echo "PINNING_CHECK_EXIT_STATUS=$pin_status"

cp /audit-output/evidence/universal-entry-spec.k \
  /tmp/audit-work/candidate-src/universal-entry-spec.k
echo '$ kprove /tmp/audit-work/candidate-src/universal-entry-spec.k --definition /tmp/audit-work/verification-kompiled --spec-module UNIVERSAL-ENTRY-SPEC'
kprove /tmp/audit-work/candidate-src/universal-entry-spec.k \
  --definition /tmp/audit-work/verification-kompiled \
  --spec-module UNIVERSAL-ENTRY-SPEC
universal_status=$?
echo "UNIVERSAL_ENTRY_PROBE_EXIT_STATUS=$universal_status"

mutation_work=/tmp/audit-work/body-sensitivity
mkdir -p "$mutation_work"
cp /tmp/audit-work/candidate-src/semantic.k "$mutation_work/semantic.k"
cp /audit-output/evidence/body-mutant-verification.k \
  "$mutation_work/body-mutant-verification.k"
cp /audit-output/evidence/body-sensitivity-spec.k \
  "$mutation_work/body-sensitivity-spec.k"

echo '$ kompile /tmp/audit-work/body-sensitivity/body-mutant-verification.k --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition /tmp/audit-work/body-sensitivity-kompiled'
kompile "$mutation_work/body-mutant-verification.k" \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition /tmp/audit-work/body-sensitivity-kompiled
mutation_build_status=$?
echo "BODY_MUTATION_KOMPILE_EXIT_STATUS=$mutation_build_status"

body_status=0
if (( mutation_build_status == 0 )); then
  echo '$ kprove /tmp/audit-work/body-sensitivity/body-sensitivity-spec.k --definition /tmp/audit-work/body-sensitivity-kompiled --spec-module BODY-SENSITIVITY-SPEC'
  kprove "$mutation_work/body-sensitivity-spec.k" \
    --definition /tmp/audit-work/body-sensitivity-kompiled \
    --spec-module BODY-SENSITIVITY-SPEC
  body_status=$?
  echo "BODY_SENSITIVITY_KPROVE_EXIT_STATUS=$body_status"
else
  body_status=125
  echo 'BODY_SENSITIVITY_KPROVE_SKIPPED=BUILD_FAILED'
fi

if (( pin_status != 0 || mutation_build_status != 0 )); then
  exit 1
fi
if (( universal_status == 0 )); then
  echo 'UNIVERSAL_ENTRY_UNEXPECTEDLY_PROVED=1'
  exit 1
fi
if (( body_status == 0 )); then
  echo 'BODY_MUTATION_UNEXPECTEDLY_PROVED=1'
  exit 1
fi
echo 'ADEQUACY_PROBES_EXPECTED_OUTCOMES=PASS'
exit 0
