#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT STATUS: %d\n' "$status"
  return "$status"
}

run python3 /audit-output/evidence/compare_program_term.py
comparison_status=$?

run python3 /audit-output/evidence/make_body_sensitivity_mutation.py
mutation_generation_status=$?

run kompile body-sensitivity-verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-sensitivity-kompiled
mutation_build_status=$?

printf '$ kprove body-sensitivity-spec.k --definition body-sensitivity-kompiled --spec-module BODY-SENSITIVITY-SPEC\n'
kprove body-sensitivity-spec.k \
  --definition body-sensitivity-kompiled \
  --spec-module BODY-SENSITIVITY-SPEC
mutation_proof_status=$?
printf 'EXIT STATUS: %d\n' "$mutation_proof_status"

printf 'PROGRAM_CONSTRUCTOR_COMPARISON_STATUS=%d\n' "$comparison_status"
printf 'BODY_MUTATION_GENERATION_STATUS=%d\n' "$mutation_generation_status"
printf 'BODY_MUTATION_BUILD_STATUS=%d\n' "$mutation_build_status"
printf 'BODY_MUTATION_PROOF_STATUS=%d (expected nonzero)\n' "$mutation_proof_status"

if (( comparison_status != 0 || mutation_generation_status != 0 || mutation_build_status != 0 )); then
  exit 1
fi
if (( mutation_proof_status == 0 )); then
  exit 1
fi
exit 0
