#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
cd "$work"

cp "$evidence/spec-vacuity.k" spec-vacuity.k
sha256sum spec-vacuity.k > "$evidence/09_vacuity_hash.log"
python3 "$evidence/09_vacuity_witness.py" \
  > "$evidence/09_vacuity_witness.log" 2>&1
witness_status=$?
printf 'EXIT_STATUS=%s\n' "$witness_status" \
  >> "$evidence/09_vacuity_witness.log"
if [ "$witness_status" -ne 0 ]; then
  exit "$witness_status"
fi

{
  printf '%s\n' \
    'COMMAND: timeout 300 kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --dry-run'
  timeout 300 kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY \
    --dry-run
  dry_status=$?
  printf 'EXIT_STATUS=%s\n' "$dry_status"
} > "$evidence/09_vacuity_dry_run.log" 2>&1
if [ "$dry_status" -ne 0 ]; then
  exit "$dry_status"
fi

{
  printf '%s\n' \
    'COMMAND: timeout 300 kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --output pretty'
  timeout 300 kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY \
    --output pretty
  proof_status=$?
  printf 'EXIT_STATUS=%s\n' "$proof_status"
} > "$evidence/09_vacuity_proof.log" 2>&1

printf 'witness_exit=%s dry_run_exit=%s mutated_proof_exit=%s\n' \
  "$witness_status" "$dry_status" "$proof_status"
test "$proof_status" -ne 0
grep -q 'WarnStuckClaimState' "$evidence/09_vacuity_proof.log"
