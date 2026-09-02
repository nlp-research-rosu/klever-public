#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
source_dir="$scratch/candidate-source"
proof_definition="$scratch/fresh-verification-kompiled"

cp "$evidence/concrete_semantics_test.py" "$scratch/concrete_semantics_test.py"

{
  printf '%s\n' \
    "COMMAND: python3 $scratch/concrete_semantics_test.py $source_dir/solution.py $source_dir/solution.mpy $proof_definition"
  python3 "$scratch/concrete_semantics_test.py" \
    "$source_dir/solution.py" "$source_dir/solution.mpy" \
    "$proof_definition"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
} > "$evidence/stage5_haskell_concrete.log" 2>&1

exit "$status"
