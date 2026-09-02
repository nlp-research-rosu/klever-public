#!/usr/bin/env bash
set -u

work=/tmp/audit-work/body-mutation
export PATH="/home/agent/.nix-profile/bin:$PATH"
cd "$work" || exit 1

echo 'MUTATION: executed parseLoopBody assigns maximum = 0 when depth exceeds maximum'
echo 'WITNESS: input "()" satisfies parenInput and fixed execution returns [0], while the unchanged postcondition requires [1]'
echo 'COMMAND: kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutated-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutated-kompiled
build_status=$?
echo "BUILD_EXIT_STATUS: $build_status"
if [ "$build_status" -ne 0 ]; then
  exit "$build_status"
fi

echo 'COMMAND: kprove spec.k --definition body-mutated-kompiled --spec-module SPEC --output pretty'
kprove spec.k \
  --definition body-mutated-kompiled \
  --spec-module SPEC \
  --output pretty
proof_status=$?
echo "PROOF_EXIT_STATUS: $proof_status"
if [ "$proof_status" -eq 0 ]; then
  echo 'BODY_SENSITIVITY=UNEXPECTED_PROOF_SUCCESS'
  exit 99
fi
echo 'BODY_SENSITIVITY=EXPECTED_PROOF_FAILURE'
exit 0
