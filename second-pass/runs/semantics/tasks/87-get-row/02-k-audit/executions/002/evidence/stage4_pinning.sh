#!/usr/bin/env bash
set -uo pipefail
set -x

work=/tmp/audit-work/rebuild
status=0
cd "$work" || exit 1

kompile body-identity-verification.k \
  --backend haskell \
  --main-module AUDIT-BODY-IDENTITY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-body-identity-kompiled
rc=$?
printf 'body_identity_fresh_kompile_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

kprove body-identity.k \
  --definition audit-body-identity-kompiled \
  --spec-module AUDIT-BODY-IDENTITY
rc=$?
printf 'body_and_closure_identity_claims_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

test -d audit-body-mutated-kompiled
rc=$?
printf 'body_mutation_prior_fresh_definition_present_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

kprove spec-shape-body-mutated.k \
  --definition audit-body-mutated-kompiled \
  --spec-module AUDIT-SHAPE-BODY-MUTATED-SPEC
rc=$?
printf 'body_mutation_expected_proof_failure_exit=%d\n' "$rc"
if (( rc == 0 )); then
  status=1
fi

printf 'stage4_pinning_exit=%d\n' "$status"
exit "$status"
