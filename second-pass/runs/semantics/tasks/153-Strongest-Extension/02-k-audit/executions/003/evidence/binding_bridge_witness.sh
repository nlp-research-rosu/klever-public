#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate || exit 97

echo "BEGIN extended_proof"
echo "COMMAND kprove spec-binding-witness.k --definition audit-strength-lemma-kompiled --spec-module BINDING-WITNESS-SPEC --claims binding-witness --output pretty"
kprove spec-binding-witness.k \
  --definition audit-strength-lemma-kompiled \
  --spec-module BINDING-WITNESS-SPEC \
  --claims binding-witness \
  --output pretty 2>&1 | tee binding-extended.out
extended_status=${PIPESTATUS[0]}
echo "EXIT extended_proof $extended_status"
if [[ $extended_status -ne 0 ]] || ! rg -qx '#Top' binding-extended.out; then
  echo "EXTENDED_THEORY_DID_NOT_ENABLE_FALSE_CONCLUSION"
  exit 1
fi

echo "BEGIN fixed_proof"
echo "COMMAND kprove spec-binding-witness.k --definition audit-verification-kompiled --spec-module BINDING-WITNESS-SPEC --claims binding-witness --output pretty"
kprove spec-binding-witness.k \
  --definition audit-verification-kompiled \
  --spec-module BINDING-WITNESS-SPEC \
  --claims binding-witness \
  --output pretty 2>&1 | tee binding-fixed.out
fixed_status=${PIPESTATUS[0]}
echo "EXIT fixed_proof $fixed_status"
if [[ $fixed_status -eq 0 ]]; then
  echo "FIXED_THEORY_UNEXPECTEDLY_PROVED_FALSE_CONCLUSION"
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' binding-fixed.out; then
  echo "FIXED_FAILURE_WAS_NOT_STUCK_CLAIM"
  exit 1
fi
if ! rg -Fq '999' binding-fixed.out; then
  echo "SHADOWED_HELPER_RESULT_NOT_VISIBLE"
  exit 1
fi
echo "FALSE_BINDING_CONCLUSION_WITNESS_CONFIRMED"
