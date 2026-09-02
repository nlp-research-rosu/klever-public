#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: kompile /audit-output/evidence/verification-bridge-mutant.k --backend haskell --main-module SUM-SQUARES-VERIFICATION-BRIDGE-MUTANT --syntax-module MPY-SYNTAX --output-definition audit-bridge-mutant-kompiled'
kompile /audit-output/evidence/verification-bridge-mutant.k \
  --backend haskell \
  --main-module SUM-SQUARES-VERIFICATION-BRIDGE-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-bridge-mutant-kompiled
build_status=$?
printf 'BUILD_EXIT_STATUS: %s\n' "$build_status"

printf '%s\n' 'COMMAND: kprove /audit-output/evidence/spec-bridge-mutant.k --definition audit-bridge-mutant-kompiled --spec-module SUM-SQUARES-SPEC-BRIDGE-MUTANT --claims SUM-SQUARES-SPEC-BRIDGE-MUTANT.mutated-loop --dry-run --output pretty'
kprove /audit-output/evidence/spec-bridge-mutant.k \
  --definition audit-bridge-mutant-kompiled \
  --spec-module SUM-SQUARES-SPEC-BRIDGE-MUTANT \
  --claims SUM-SQUARES-SPEC-BRIDGE-MUTANT.mutated-loop \
  --dry-run \
  --output pretty
dry_status=$?
printf 'DRY_RUN_EXIT_STATUS: %s\n' "$dry_status"

printf '%s\n' 'COMMAND: kprove /audit-output/evidence/spec-bridge-mutant.k --definition audit-bridge-mutant-kompiled --spec-module SUM-SQUARES-SPEC-BRIDGE-MUTANT --claims SUM-SQUARES-SPEC-BRIDGE-MUTANT.mutated-loop --output pretty'
set +e
kprove /audit-output/evidence/spec-bridge-mutant.k \
  --definition audit-bridge-mutant-kompiled \
  --spec-module SUM-SQUARES-SPEC-BRIDGE-MUTANT \
  --claims SUM-SQUARES-SPEC-BRIDGE-MUTANT.mutated-loop \
  --output pretty 2>&1 | tee bridge-mutant-backend-output.tmp
proof_status=${PIPESTATUS[0]}
set -e
printf 'PROOF_EXIT_STATUS: %s\n' "$proof_status"

grep -q 'WarnStuckClaimState' bridge-mutant-backend-output.tmp
stuck_status=$?
printf 'WARN_STUCK_PRESENT: %s\n' "$((stuck_status == 0))"

if (( build_status == 0 && dry_status == 0 && proof_status != 0 && stuck_status == 0 )); then
  printf '%s\n' 'OPERATIONAL_SENSITIVITY_REJECTION: PASS'
  exit 0
fi
printf '%s\n' 'OPERATIONAL_SENSITIVITY_REJECTION: FAIL'
exit 1
