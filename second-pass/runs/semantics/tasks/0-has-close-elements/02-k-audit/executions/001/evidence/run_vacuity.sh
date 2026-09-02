#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/0-has-close-elements
evidence=/audit-output/evidence
cp "$evidence/spec-vacuity-audit.k" "$scratch/spec-vacuity-audit.k"

run_and_log() {
  log=$1
  shift
  {
    printf 'WORKDIR: %s\n' "$scratch"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } > "$evidence/$log"
  (
    cd "$scratch" || exit 125
    "$@"
  ) >> "$evidence/$log" 2>&1
  status=$?
  printf 'EXIT: %s\n' "$status" >> "$evidence/$log"
  printf '%s exit=%s\n' "$log" "$status"
  return "$status"
}

# Parsing and KORE generation must succeed.
run_and_log 06a-vacuity-dry-run.log \
  kprove spec-vacuity-audit.k \
  --definition audit-build/entry-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
dry_status=$?

# The actual proof must fail with an unmet result condition.
run_and_log 06b-vacuity-proof.log \
  kprove spec-vacuity-audit.k \
  --definition audit-build/entry-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
proof_status=$?

{
  printf '%s\n' 'SATISFYING WITNESS: numbers=[1.0, 1.0], threshold=0.1'
  printf '%s\n' 'Original claimed result: true (abs(1.0 - 1.0) < 0.1).'
  printf '%s\n' 'Mutated demanded result: false.'
  printf 'dry_run_exit=%s\n' "$dry_status"
  printf 'proof_exit=%s\n' "$proof_status"
} > "$evidence/06c-vacuity-witness.txt"

if [[ $dry_status -eq 0 && $proof_status -ne 0 ]]; then
  exit 0
fi
exit 1
