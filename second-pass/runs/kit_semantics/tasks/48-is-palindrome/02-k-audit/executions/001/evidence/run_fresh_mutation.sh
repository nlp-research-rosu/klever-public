#!/usr/bin/env bash
set -u

work=/tmp/audit-work/48-is-palindrome-audit
cd "$work" || exit 90
cp /audit-output/evidence/spec-reviewer-false.k spec-reviewer-false.k

printf 'COMMAND: kprove spec-reviewer-false.k --definition verification-review4-kompiled --spec-module SPEC-REVIEWER-FALSE --dry-run\n'
kprove spec-reviewer-false.k \
  --definition verification-review4-kompiled \
  --spec-module SPEC-REVIEWER-FALSE \
  --dry-run
dry_status=$?
printf 'DRY_RUN_EXIT_STATUS=%s\n' "$dry_status"
[[ "$dry_status" -eq 0 ]] || exit 91

printf 'COMMAND: kprove spec-reviewer-false.k --definition verification-review4-kompiled --spec-module SPEC-REVIEWER-FALSE --claims SPEC-REVIEWER-FALSE.empty-must-be-false\n'
kprove spec-reviewer-false.k \
  --definition verification-review4-kompiled \
  --spec-module SPEC-REVIEWER-FALSE \
  --claims SPEC-REVIEWER-FALSE.empty-must-be-false \
  > reviewer-false-proof.out 2>&1
proof_status=$?
printf 'PROOF_EXIT_STATUS=%s\n' "$proof_status"
sed -n '1,260p' reviewer-false-proof.out

if [[ "$proof_status" -eq 0 ]]; then
  printf 'ERROR: false obligation unexpectedly proved\n'
  exit 92
fi
if ! rg -q 'WarnStuckClaimState' reviewer-false-proof.out; then
  printf 'ERROR: expected stuck-claim diagnostic absent\n'
  exit 93
fi
if ! rg -q '"__result"[[:space:]]*\\|->[[:space:]]*true' reviewer-false-proof.out; then
  printf 'ERROR: residual did not expose actual true result\n'
  exit 94
fi
printf 'EXPECTED_FAILURE_CONFIRMED=YES\n'
printf 'FRESH_NON_VACUITY_RESULT=PASS\n'
