#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
source_dir="$scratch/candidate-source"
semantic_definition="$scratch/fresh-semantic-kompiled"

cp "$evidence/concrete_semantics_test.py" "$scratch/concrete_semantics_test.py"

{
  printf '%s\n' \
    "COMMAND: python3 $scratch/concrete_semantics_test.py $source_dir/solution.py $source_dir/solution.mpy $semantic_definition"
  python3 "$scratch/concrete_semantics_test.py" \
    "$source_dir/solution.py" "$source_dir/solution.mpy" \
    "$semantic_definition"
  concrete_status=$?
  printf 'EXIT_STATUS: %d\n' "$concrete_status"
} > "$evidence/stage3_concrete.log" 2>&1

exit "$concrete_status"
