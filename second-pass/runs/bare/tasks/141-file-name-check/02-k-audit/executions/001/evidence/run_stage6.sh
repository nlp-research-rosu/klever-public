#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
source_dir="$scratch/candidate-source"
proof_definition="$scratch/fresh-verification-kompiled"

cp "$evidence/audit-false-spec.k" "$source_dir/audit-false-spec.k"

{
  printf '%s\n' \
    "COMMAND: kprove audit-false-spec.k --definition $proof_definition --spec-module AUDIT-FALSE-SPEC --dry-run"
  (
    cd "$source_dir" &&
    kprove audit-false-spec.k \
      --definition "$proof_definition" \
      --spec-module AUDIT-FALSE-SPEC \
      --dry-run
  )
  dry_run_status=$?
  printf 'DRY_RUN_EXIT_STATUS: %d\n' "$dry_run_status"

  printf '%s\n' \
    "COMMAND: kprove audit-false-spec.k --definition $proof_definition --spec-module AUDIT-FALSE-SPEC"
  (
    cd "$source_dir" &&
    kprove audit-false-spec.k \
      --definition "$proof_definition" \
      --spec-module AUDIT-FALSE-SPEC
  )
  mutation_status=$?
  printf 'PROOF_EXIT_STATUS: %d\n' "$mutation_status"
} > "$evidence/stage6_false_mutation.log" 2>&1

if (( dry_run_status != 0 )); then
  exit 1
fi
if (( mutation_status == 0 )); then
  exit 1
fi
