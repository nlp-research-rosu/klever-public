#!/usr/bin/env bash
set -uo pipefail

SCRATCH=/tmp/audit-work/59-lpf
EVIDENCE=/audit-output/evidence
cd "$SCRATCH" || exit 1

echo "$ kompile verification-body-mutation.k --backend haskell --main-module VERIFICATION-BODY-MUTATION --syntax-module MPY-SYNTAX --output-definition audit-body-mutation-kompiled"
kompile verification-body-mutation.k \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-body-mutation-kompiled \
  > "$EVIDENCE/06_body_mutation_kompile.log" 2>&1
build_status=$?
echo "kompile_exit=$build_status"
if [ "$build_status" -ne 0 ]; then
  tail -120 "$EVIDENCE/06_body_mutation_kompile.log"
  exit "$build_status"
fi

echo "$ kprove spec-body-mutation.k --definition audit-body-mutation-kompiled --spec-module SPEC-BODY-MUTATION --claims SPEC-BODY-MUTATION.largest-prime-factor-entry"
kprove spec-body-mutation.k \
  --definition audit-body-mutation-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --claims SPEC-BODY-MUTATION.largest-prime-factor-entry \
  > "$EVIDENCE/06_body_mutation_kprove.log" 2>&1
proof_status=$?
echo "kprove_exit=$proof_status"
tail -160 "$EVIDENCE/06_body_mutation_kprove.log"

if [ "$proof_status" -eq 0 ]; then
  echo "ERROR: body mutation unexpectedly proved"
  exit 1
fi
if ! rg -q 'WarnStuckClaimState|cannot be rewritten further' "$EVIDENCE/06_body_mutation_kprove.log"; then
  echo "ERROR: failure was not an expected stuck claim"
  exit 1
fi
echo "expected_body_sensitivity_failure_observed=true"
