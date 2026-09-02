#!/usr/bin/env bash
set -u

work=/tmp/audit-work/48-is-palindrome-audit
cd "$work" || exit 90
cp /audit-output/evidence/spec-reviewer-body-mutation.k \
  spec-reviewer-body-mutation.k

printf 'COMMAND: kprove spec-reviewer-body-mutation.k --definition verification-review4-kompiled --spec-module SPEC-REVIEWER-BODY-MUTATION --dry-run\n'
kprove spec-reviewer-body-mutation.k \
  --definition verification-review4-kompiled \
  --spec-module SPEC-REVIEWER-BODY-MUTATION \
  --dry-run
dry_status=$?
printf 'DRY_RUN_EXIT_STATUS=%s\n' "$dry_status"
[[ "$dry_status" -eq 0 ]] || exit 91

printf 'COMMAND: kprove spec-reviewer-body-mutation.k --definition verification-review4-kompiled --spec-module SPEC-REVIEWER-BODY-MUTATION --claims SPEC-REVIEWER-BODY-MUTATION.mutated-body-empty-true\n'
kprove spec-reviewer-body-mutation.k \
  --definition verification-review4-kompiled \
  --spec-module SPEC-REVIEWER-BODY-MUTATION \
  --claims SPEC-REVIEWER-BODY-MUTATION.mutated-body-empty-true \
  > reviewer-body-mutation-proof.out 2>&1
proof_status=$?
printf 'PROOF_EXIT_STATUS=%s\n' "$proof_status"
sed -n '1,240p' reviewer-body-mutation-proof.out

if [[ "$proof_status" -eq 0 ]]; then
  printf 'ERROR: body mutation unexpectedly proved\n'
  exit 92
fi
if ! rg -q 'WarnStuckClaimState' reviewer-body-mutation-proof.out; then
  printf 'ERROR: expected stuck-claim diagnostic absent\n'
  exit 93
fi
if ! rg -q '"__result"[[:space:]]*\\|->[[:space:]]*false' reviewer-body-mutation-proof.out; then
  printf 'ERROR: residual did not expose mutated false result\n'
  exit 94
fi
printf 'BODY_SENSITIVITY_RESULT=PASS\n'
