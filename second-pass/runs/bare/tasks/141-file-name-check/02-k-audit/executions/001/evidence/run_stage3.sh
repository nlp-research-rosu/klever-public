#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
source_dir="$scratch/candidate-source"
semantic_definition="$scratch/fresh-semantic-kompiled"
proof_definition="$scratch/fresh-verification-kompiled"

cp "$evidence/concrete_semantics_test.py" "$scratch/concrete_semantics_test.py"

{
  printf '%s\n' \
    "COMMAND: kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --backend llvm --output-definition $semantic_definition"
  (
    cd "$source_dir" &&
    kompile semantic.k \
      --main-module SEMANTIC \
      --syntax-module MPY-SYNTAX \
      --backend llvm \
      --output-definition "$semantic_definition"
  )
  semantic_build_status=$?
  printf 'EXIT_STATUS: %d\n' "$semantic_build_status"
} > "$evidence/stage3_semantic_build.log" 2>&1

if (( semantic_build_status == 0 )); then
  {
    printf '%s\n' \
      "COMMAND: python3 $scratch/concrete_semantics_test.py $source_dir/solution.py $source_dir/solution.mpy $semantic_definition"
    python3 "$scratch/concrete_semantics_test.py" \
      "$source_dir/solution.py" "$source_dir/solution.mpy" \
      "$semantic_definition"
    concrete_status=$?
    printf 'EXIT_STATUS: %d\n' "$concrete_status"
  } > "$evidence/stage3_concrete.log" 2>&1
else
  concrete_status=125
  printf 'SKIPPED: semantic build failed\nEXIT_STATUS: 125\n' \
    > "$evidence/stage3_concrete.log"
fi

{
  printf '%s\n' \
    "COMMAND: kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition $proof_definition"
  (
    cd "$source_dir" &&
    kompile verification.k \
      --main-module VERIFICATION \
      --syntax-module MPY-SYNTAX \
      --backend haskell \
      --output-definition "$proof_definition"
  )
  proof_build_status=$?
  printf 'EXIT_STATUS: %d\n' "$proof_build_status"
} > "$evidence/stage3_proof_build.log" 2>&1

if (( proof_build_status == 0 )); then
  {
    printf '%s\n' \
      "COMMAND: kprove spec.k --definition $proof_definition --spec-module SPEC"
    (
      cd "$source_dir" &&
      kprove spec.k \
        --definition "$proof_definition" \
        --spec-module SPEC
    )
    proof_status=$?
    printf 'EXIT_STATUS: %d\n' "$proof_status"
  } > "$evidence/stage3_positive_proof.log" 2>&1
else
  proof_status=125
  printf 'SKIPPED: proof definition build failed\nEXIT_STATUS: 125\n' \
    > "$evidence/stage3_positive_proof.log"
fi

if (( semantic_build_status != 0 || concrete_status != 0 ||
      proof_build_status != 0 || proof_status != 0 )); then
  exit 1
fi
