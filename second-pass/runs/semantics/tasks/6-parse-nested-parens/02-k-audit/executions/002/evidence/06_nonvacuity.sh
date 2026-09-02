#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
export PATH="/home/agent/.nix-profile/bin:$PATH"
cd "$work" || exit 1

echo 'MUTATION: append an extra trailing 0 to the result-constraining heap value'
echo 'SATISFYING_WITNESS: S codes "()" satisfy parenInput; actual=[1], false obligation=[1,0]'
echo 'COMMAND: kprove spec-vacuity-audit.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY-AUDIT --dry-run --output none'
kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run \
  --output none
build_status=$?
echo "MUTATION_BUILD_EXIT_STATUS: $build_status"
if [ "$build_status" -ne 0 ]; then
  exit "$build_status"
fi

echo 'COMMAND: kprove spec-vacuity-audit.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY-AUDIT --output pretty'
kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --output pretty
proof_status=$?
echo "MUTATION_PROOF_EXIT_STATUS: $proof_status"
if [ "$proof_status" -eq 0 ]; then
  echo 'NONVACUITY=UNEXPECTED_FALSE_CLAIM_SUCCESS'
  exit 99
fi
echo 'NONVACUITY=EXPECTED_FALSE_CLAIM_FAILURE'
exit 0
