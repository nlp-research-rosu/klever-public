#!/usr/bin/env bash
set -u

cd /tmp/audit-work/body-mutation || exit 97

echo "MUTATION"
diff -u /tmp/audit-work/candidate/verification.k verification.k
diff_status=$?
echo "EXIT mutation_diff $diff_status"
if [[ $diff_status -ne 1 ]]; then
  echo "Expected exactly one source difference."
  exit 1
fi

echo "BEGIN build_body_mutation"
echo "COMMAND kompile verification.k --backend haskell --main-module STRONGEST-EXTENSION-WITH-LOOP-LEMMAS --syntax-module MPY-SYNTAX --output-definition audit-body-mutated-2-kompiled -I ."
kompile verification.k \
  --backend haskell \
  --main-module STRONGEST-EXTENSION-WITH-LOOP-LEMMAS \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-body-mutated-2-kompiled \
  -I .
build_status=$?
echo "EXIT build_body_mutation $build_status"
if [[ $build_status -ne 0 ]]; then
  exit 1
fi

echo "BEGIN prove_unchanged_entry_against_mutated_body"
echo "COMMAND kprove spec.k --definition audit-body-mutated-2-kompiled --spec-module STRONGEST-EXTENSION-SPEC --claims strongest-extension-correct --output pretty"
kprove spec.k \
  --definition audit-body-mutated-2-kompiled \
  --spec-module STRONGEST-EXTENSION-SPEC \
  --claims strongest-extension-correct \
  --output pretty 2>&1 | tee body-mutation-proof.out
proof_status=${PIPESTATUS[0]}
echo "EXIT prove_unchanged_entry_against_mutated_body $proof_status"
if [[ $proof_status -eq 0 ]]; then
  echo "UNEXPECTED_SUCCESS"
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' body-mutation-proof.out; then
  echo "FAILURE_WAS_NOT_STUCK_CLAIM"
  exit 1
fi
if ! rg -Fq 'iCons ( 33' body-mutation-proof.out; then
  echo "EXPECTED_MUTATED_EXCLAMATION_RESULT_NOT_VISIBLE"
  exit 1
fi
echo "EXPECTED_BODY_SENSITIVITY_FAILURE"
