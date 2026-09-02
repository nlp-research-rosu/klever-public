#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
original="$scratch/candidate-source"
mutation="$scratch/body-mutation"
definition="$scratch/body-mutation-kompiled"

mkdir -p "$mutation"
cp "$original/semantic.k" "$original/verification.k" "$original/spec.k" "$mutation/"

{
  printf '%s\n' \
    "COMMAND: patch --directory=$mutation --input=$evidence/body-sensitivity.patch"
  patch --directory="$mutation" --input="$evidence/body-sensitivity.patch"
  patch_status=$?
  printf 'PATCH_EXIT_STATUS: %d\n' "$patch_status"

  printf '%s\n' \
    "COMMAND: kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition $definition"
  (
    cd "$mutation" &&
    kompile verification.k \
      --main-module VERIFICATION \
      --syntax-module MPY-SYNTAX \
      --backend haskell \
      --output-definition "$definition"
  )
  build_status=$?
  printf 'BUILD_EXIT_STATUS: %d\n' "$build_status"

  if (( build_status == 0 )); then
    printf '%s\n' \
      "COMMAND: kprove spec.k --definition $definition --spec-module SPEC"
    (
      cd "$mutation" &&
      kprove spec.k \
        --definition "$definition" \
        --spec-module SPEC
    )
    proof_status=$?
  else
    proof_status=125
    printf '%s\n' 'SKIPPED: mutated definition did not build'
  fi
  printf 'PROOF_EXIT_STATUS: %d\n' "$proof_status"
} > "$evidence/stage5_body_sensitivity.log" 2>&1

if (( patch_status != 0 || build_status != 0 )); then
  exit 1
fi
if (( proof_status == 0 )); then
  exit 1
fi
