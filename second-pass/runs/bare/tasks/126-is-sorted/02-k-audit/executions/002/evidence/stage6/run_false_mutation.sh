#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/candidate-fresh
definition="$scratch/verification-haskell-kompiled"
spec="$scratch/audit-false-spec.k"
dry_log=/audit-output/evidence/stage6/false-mutation-dry-run.log
proof_log=/audit-output/evidence/stage6/false-mutation-proof.log

echo 'COMMAND: cmp -s scratch/audit-false-spec.k evidence/stage6/audit-false-spec.k'
cmp -s "$spec" /audit-output/evidence/stage6/audit-false-spec.k
copy_status=$?
echo "PRESERVED_MUTATION_IDENTITY_EXIT_STATUS=$copy_status"
if [[ "$copy_status" -ne 0 ]]; then
  exit "$copy_status"
fi

echo 'MUTATION: executed program limit Int(2) -> Int(1); original postcondition retained'
echo 'SATISFYING_WITNESS: input IS = Cons(0, Cons(0, Nil)); original result = true; mutated result = false'
echo 'COMMAND: kprove audit-false-spec.k --definition verification-haskell-kompiled --spec-module AUDIT-FALSE-SPEC --dry-run'
(
  cd "$scratch" &&
  kprove \
    audit-false-spec.k \
    --definition "$definition" \
    --spec-module AUDIT-FALSE-SPEC \
    --dry-run
) 2>&1 | tee "$dry_log"
dry_status=${PIPESTATUS[0]}
echo "DRY_RUN_EXIT_STATUS=$dry_status" | tee -a "$dry_log"
if [[ "$dry_status" -ne 0 ]]; then
  echo 'ERROR: mutation did not build/parse successfully'
  exit 2
fi

echo 'COMMAND: kprove audit-false-spec.k --definition verification-haskell-kompiled --spec-module AUDIT-FALSE-SPEC'
(
  cd "$scratch" &&
  kprove \
    audit-false-spec.k \
    --definition "$definition" \
    --spec-module AUDIT-FALSE-SPEC
) 2>&1 | tee "$proof_log"
proof_status=${PIPESTATUS[0]}
echo "MUTATED_PROOF_EXIT_STATUS=$proof_status" | tee -a "$proof_log"

if [[ "$proof_status" -eq 0 ]]; then
  echo 'ERROR: false mutation unexpectedly closed'
  exit 3
fi

rg -q 'WarnStuckClaimState' "$proof_log"
stuck_status=$?
echo "HAS_EXPECTED_STUCK_WARNING=$([[ $stuck_status -eq 0 ]] && echo true || echo false)" \
  | tee -a "$proof_log"
rg -q 'BoolVal' "$proof_log"
bool_residual_status=$?
echo "HAS_BOOLVAL_RESIDUAL=$([[ $bool_residual_status -eq 0 ]] && echo true || echo false)" \
  | tee -a "$proof_log"
rg -q 'parser|Parse error|Could not find module|No such file' "$proof_log"
unrelated_status=$?
echo "HAS_UNRELATED_PARSE_OR_IMPORT_ERROR=$([[ $unrelated_status -eq 0 ]] && echo true || echo false)" \
  | tee -a "$proof_log"

if [[
  "$stuck_status" -ne 0
  || "$bool_residual_status" -ne 0
  || "$unrelated_status" -eq 0
 ]]; then
  echo 'ERROR: failure was not the expected unmet boolean obligation'
  exit 4
fi
exit 0
