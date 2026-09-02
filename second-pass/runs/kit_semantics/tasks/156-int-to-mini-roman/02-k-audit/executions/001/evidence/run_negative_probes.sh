#!/usr/bin/env bash
set -u

cd /tmp/audit-work/rebuild || exit 1

bash /audit-output/evidence/run_capture.sh \
  /audit-output/evidence/kompile_body_mutant.log \
  kompile --backend haskell verification-body-mutant.k \
    --main-module VERIFICATION-BODY-MUTANT \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-body-mutant-kompiled
compile_rc=$?
if [ "$compile_rc" -ne 0 ]; then
  printf 'BODY_MUTANT_BUILD=FAIL rc=%s\n' "$compile_rc"
  exit 1
fi

bash /audit-output/evidence/run_capture.sh \
  /audit-output/evidence/kprove_body_mutant.log \
  kprove spec-body-mutant.k \
    --definition verification-body-mutant-kompiled \
    --spec-module SPEC-BODY-MUTANT
body_rc=$?
if [ "$body_rc" -eq 0 ]; then
  printf 'BODY_SENSITIVITY=FAIL unexpected proof success\n'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' /audit-output/evidence/kprove_body_mutant.log; then
  printf 'BODY_SENSITIVITY=FAIL no stuck-claim residual rc=%s\n' "$body_rc"
  exit 1
fi
printf 'BODY_SENSITIVITY=PASS expected_stuck_rc=%s\n' "$body_rc"

bash /audit-output/evidence/run_capture.sh \
  /audit-output/evidence/kprove_false_dry_run.log \
  kprove spec-false.k \
    --definition verification-kompiled \
    --spec-module SPEC-FALSE \
    --dry-run
dry_rc=$?
if [ "$dry_rc" -ne 0 ]; then
  printf 'FALSE_MUTATION_BUILD=FAIL rc=%s\n' "$dry_rc"
  exit 1
fi
printf 'FALSE_MUTATION_BUILD=PASS rc=0\n'

bash /audit-output/evidence/run_capture.sh \
  /audit-output/evidence/kprove_false.log \
  kprove spec-false.k \
    --definition verification-kompiled \
    --spec-module SPEC-FALSE
false_rc=$?
if [ "$false_rc" -eq 0 ]; then
  printf 'NONVACUITY=FAIL false obligation proved\n'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' /audit-output/evidence/kprove_false.log; then
  printf 'NONVACUITY=FAIL no stuck-claim residual rc=%s\n' "$false_rc"
  exit 1
fi
printf 'NONVACUITY=PASS expected_stuck_rc=%s witness=4 true=iv false=v\n' \
  "$false_rc"
