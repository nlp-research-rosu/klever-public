#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate || exit 97

echo "SATISFYING_WITNESS class_name=my_class extensions=[AA,Be,CC]"
echo "TRUE_RESULT my_class.AA"
echo "MUTATED_REQUIRED_RESULT my_class!AA"

echo "BEGIN mutation_dry_run"
echo "COMMAND kprove spec-vacuity.k --definition audit-loop-lemmas-kompiled --spec-module STRONGEST-EXTENSION-SPEC-VACUITY --claims false-separator --dry-run"
kprove spec-vacuity.k \
  --definition audit-loop-lemmas-kompiled \
  --spec-module STRONGEST-EXTENSION-SPEC-VACUITY \
  --claims false-separator \
  --dry-run 2>&1 | tee vacuity-dry-run.out
dry_status=${PIPESTATUS[0]}
echo "EXIT mutation_dry_run $dry_status"
if [[ $dry_status -ne 0 ]]; then
  echo "MUTATION_DID_NOT_BUILD"
  exit 1
fi

echo "BEGIN mutation_proof"
echo "COMMAND kprove spec-vacuity.k --definition audit-loop-lemmas-kompiled --spec-module STRONGEST-EXTENSION-SPEC-VACUITY --claims false-separator --output pretty"
kprove spec-vacuity.k \
  --definition audit-loop-lemmas-kompiled \
  --spec-module STRONGEST-EXTENSION-SPEC-VACUITY \
  --claims false-separator \
  --output pretty 2>&1 | tee vacuity-proof.out
proof_status=${PIPESTATUS[0]}
echo "EXIT mutation_proof $proof_status"
if [[ $proof_status -eq 0 ]]; then
  echo "UNEXPECTED_MUTATION_SUCCESS"
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' vacuity-proof.out; then
  echo "FAILURE_WAS_NOT_STUCK_CLAIM"
  exit 1
fi
if ! rg -Fq 'iCons ( 46' vacuity-proof.out || ! rg -Fq 'iCons ( 33' vacuity-proof.out; then
  echo "EXPECTED_SEPARATOR_OBLIGATION_NOT_VISIBLE"
  exit 1
fi
echo "EXPECTED_NON_VACUITY_FAILURE"
