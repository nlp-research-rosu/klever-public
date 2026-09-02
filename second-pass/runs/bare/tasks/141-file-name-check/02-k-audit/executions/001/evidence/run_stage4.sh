#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
source_dir="$scratch/candidate-source"
proof_definition="$scratch/fresh-verification-kompiled"

cp "$evidence/program_identity_check.py" "$scratch/program_identity_check.py"
cp "$evidence/audit-ground-spec.k" "$source_dir/audit-ground-spec.k"

{
  printf '%s\n' \
    "COMMAND: python3 $scratch/program_identity_check.py $source_dir/verification.k $source_dir/solution.mpy"
  python3 "$scratch/program_identity_check.py" \
    "$source_dir/verification.k" "$source_dir/solution.mpy"
  identity_status=$?
  printf 'EXIT_STATUS: %d\n' "$identity_status"

  printf '%s\n' \
    "COMMAND: kprove audit-ground-spec.k --definition $proof_definition --spec-module AUDIT-GROUND-SPEC"
  (
    cd "$source_dir" &&
    kprove audit-ground-spec.k \
      --definition "$proof_definition" \
      --spec-module AUDIT-GROUND-SPEC
  )
  ground_status=$?
  printf 'EXIT_STATUS: %d\n' "$ground_status"

  printf '%s\n' \
    "COMMAND: krun solution.mpy --definition $proof_definition -cINPUT='\"A.dll\"'"
  (
    cd "$source_dir" &&
    krun solution.mpy \
      --definition "$proof_definition" \
      -cINPUT='"A.dll"'
  )
  ground_krun_status=$?
  printf 'EXIT_STATUS: %d\n' "$ground_krun_status"

  printf '%s\n' \
    "COMMAND: krun solution.mpy --definition $proof_definition -cINPUT='\"\"'"
  (
    cd "$source_dir" &&
    krun solution.mpy \
      --definition "$proof_definition" \
      -cINPUT='""'
  )
  empty_krun_status=$?
  printf 'EXIT_STATUS: %d\n' "$empty_krun_status"
} > "$evidence/stage4_pinning.log" 2>&1

# The empty-input failure is recorded candidate evidence, not a runner error.
if (( identity_status != 0 || ground_status != 0 ||
      ground_krun_status != 0 )); then
  exit 1
fi
