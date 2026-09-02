#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/95-check-dict-case-audit
cp /audit-output/evidence/program-body-mutation.k "$scratch/"
cp /audit-output/evidence/verification-body-mutation.k "$scratch/"
cp /audit-output/evidence/spec-body-mutation.k "$scratch/"

printf '%s\n' \
  'COMMAND: kompile verification-body-mutation.k --main-module VERIFICATION-BODY-MUTATION --syntax-module VERIFICATION-BODY-MUTATION --backend haskell --output-definition verification-body-mutation-kompiled'
(
  cd "$scratch" || exit 1
  kompile verification-body-mutation.k \
    --main-module VERIFICATION-BODY-MUTATION \
    --syntax-module VERIFICATION-BODY-MUTATION \
    --backend haskell \
    --output-definition verification-body-mutation-kompiled
)
build_status=$?
printf 'BODY_MUTATION_BUILD_EXIT=%s\n' "$build_status"
if [[ "$build_status" -ne 0 ]]; then
  exit "$build_status"
fi

printf '%s\n' \
  'COMMAND: kprove spec-body-mutation.k --definition verification-body-mutation-kompiled --spec-module SPEC-BODY-MUTATION'
(
  cd "$scratch" || exit 1
  kprove spec-body-mutation.k \
    --definition verification-body-mutation-kompiled \
    --spec-module SPEC-BODY-MUTATION
)
proof_status=$?
printf 'BODY_MUTATION_PROOF_EXIT=%s\n' "$proof_status"
if [[ "$proof_status" -eq 0 ]]; then
  printf '%s\n' 'BODY_SENSITIVITY=FAILED_MUTATION_UNEXPECTEDLY_PROVED'
  exit 1
fi
printf '%s\n' 'BODY_SENSITIVITY=PASS_EXPECTED_PROOF_FAILURE'
exit 0
