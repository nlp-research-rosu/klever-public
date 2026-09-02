#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
cd "$work"

cp "$evidence/verification-body-mutation.k" verification-body-mutation.k
cp "$evidence/spec-body-mutation.k" spec-body-mutation.k
sha256sum verification-body-mutation.k spec-body-mutation.k \
  > "$evidence/08_body_mutation_hashes.log"

{
  printf '%s\n' \
    'COMMAND: timeout 900 kompile verification-body-mutation.k --backend haskell --main-module VERIFICATION-BODY-MUTATION --syntax-module MPY-SYNTAX --output-definition verification-body-mutation-kompiled'
  timeout 900 kompile verification-body-mutation.k \
    --backend haskell \
    --main-module VERIFICATION-BODY-MUTATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-body-mutation-kompiled
  build_status=$?
  printf 'EXIT_STATUS=%s\n' "$build_status"
} > "$evidence/08_body_mutation_build.log" 2>&1
if [ "$build_status" -ne 0 ]; then
  exit "$build_status"
fi

{
  printf '%s\n' \
    'COMMAND: timeout 300 kprove spec-body-mutation.k --definition verification-body-mutation-kompiled --spec-module SPEC-BODY-MUTATION --output pretty'
  timeout 300 kprove spec-body-mutation.k \
    --definition verification-body-mutation-kompiled \
    --spec-module SPEC-BODY-MUTATION \
    --output pretty
  proof_status=$?
  printf 'EXIT_STATUS=%s\n' "$proof_status"
} > "$evidence/08_body_mutation_proof.log" 2>&1

printf 'build_exit=%s body_mutation_proof_exit=%s\n' \
  "$build_status" "$proof_status"
test "$proof_status" -ne 0
grep -q 'WarnStuckClaimState' "$evidence/08_body_mutation_proof.log"
