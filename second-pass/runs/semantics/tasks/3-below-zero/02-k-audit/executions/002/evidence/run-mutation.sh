#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
cd "$work" || exit 1

printf '%s\n' \
  'COMMAND: kprove spec-audit-mutation.k --definition verification-lemma-kompiled --spec-module AUDIT-MUTATION --dry-run' |
  tee "$evidence/06a-mutation-dry-run.log"
kprove spec-audit-mutation.k \
  --definition verification-lemma-kompiled \
  --spec-module AUDIT-MUTATION \
  --dry-run 2>&1 | tee -a "$evidence/06a-mutation-dry-run.log"
dry_status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %s\n' "$dry_status" |
  tee -a "$evidence/06a-mutation-dry-run.log"
if [[ $dry_status -ne 0 ]]; then
  printf 'MUTATION_RESULT: invalid; dry run failed\n'
  exit 1
fi

printf '%s\n' \
  'COMMAND: kprove spec-audit-mutation.k --definition verification-lemma-kompiled --spec-module AUDIT-MUTATION' |
  tee "$evidence/06b-mutation-proof.log"
kprove spec-audit-mutation.k \
  --definition verification-lemma-kompiled \
  --spec-module AUDIT-MUTATION \
  2>&1 | tee -a "$evidence/06b-mutation-proof.log"
proof_status=${PIPESTATUS[0]}
printf 'EXIT_STATUS: %s\n' "$proof_status" |
  tee -a "$evidence/06b-mutation-proof.log"

if [[ $proof_status -eq 0 ]]; then
  printf 'MUTATION_RESULT: invalid; false mutation unexpectedly closed\n'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState|cannot be rewritten further|implication check' \
  "$evidence/06b-mutation-proof.log"; then
  printf 'MUTATION_RESULT: invalid; failure lacked expected unmet-obligation residual\n'
  exit 1
fi
printf 'MUTATION_RESULT: expected proof failure with unmet result obligation\n'
exit 0
