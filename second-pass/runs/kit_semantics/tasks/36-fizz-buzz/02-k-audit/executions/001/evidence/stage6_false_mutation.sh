#!/usr/bin/env bash
set +e

printf 'WITNESS: N=79, submitted=3, trusted_canonical=3, mutated_required_result=5\n'

printf 'COMMAND: kprove audit-spec-false.k --definition audit-verification-kompiled --spec-module AUDIT-SPEC-FALSE --dry-run > audit-spec-false.kore\n'
kprove audit-spec-false.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-FALSE \
  --dry-run > audit-spec-false.kore 2> /audit-output/evidence/stage6_false_mutation_dry_run.stderr
dry_status=$?
printf 'EXIT STATUS: %s\n' "$dry_status"
if [ "$dry_status" -ne 0 ]; then
  sed -n '1,200p' /audit-output/evidence/stage6_false_mutation_dry_run.stderr
  exit "$dry_status"
fi
printf 'DRY-RUN KORE BYTES: %s\n' "$(wc -c < audit-spec-false.kore)"
sed -n '1,120p' /audit-output/evidence/stage6_false_mutation_dry_run.stderr

printf 'COMMAND: kprove audit-spec-false.k --definition audit-verification-kompiled --spec-module AUDIT-SPEC-FALSE\n'
kprove audit-spec-false.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-FALSE \
  > /audit-output/evidence/stage6_false_mutation_prover.log 2>&1
prove_status=$?
printf 'EXIT STATUS: %s\n' "$prove_status"
sed -n '1,240p' /audit-output/evidence/stage6_false_mutation_prover.log

if [ "$prove_status" -eq 0 ]; then
  printf 'AUDIT ERROR: false mutation unexpectedly closed\n'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' /audit-output/evidence/stage6_false_mutation_prover.log; then
  printf 'AUDIT ERROR: expected stuck-claim diagnostic was absent\n'
  exit 1
fi
if ! rg -q 'backend terminated because' /audit-output/evidence/stage6_false_mutation_prover.log || \
   ! rg -q 'rewritten further' /audit-output/evidence/stage6_false_mutation_prover.log; then
  printf 'AUDIT ERROR: expected unmet-obligation termination was absent\n'
  exit 1
fi
printf 'EXPECTED RESULT: dry-run built; false reachable obligation was rejected with a stuck claim\n'
