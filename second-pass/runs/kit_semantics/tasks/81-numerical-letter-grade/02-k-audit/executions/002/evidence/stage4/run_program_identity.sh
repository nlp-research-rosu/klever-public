#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate-src || exit 90

printf '$ kast --definition audit-verification-kompiled --module VERIFICATION --sort Module --expand-macros --output kore solution.mpy > audit-solution-term.kore\n'
kast --definition audit-verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  solution.mpy > audit-solution-term.kore
solution_rc=$?
printf 'EXIT kast_solution=%s\n' "$solution_rc"

printf '$ kast --definition audit-verification-kompiled --module VERIFICATION --sort Module --expand-macros --output kore --expression GRADE-PROGRAM > audit-proof-term.kore\n'
kast --definition audit-verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  --expression 'GRADE-PROGRAM' > audit-proof-term.kore
proof_rc=$?
printf 'EXIT kast_proof_macro=%s\n' "$proof_rc"

printf '$ cmp -s audit-solution-term.kore audit-proof-term.kore\n'
cmp -s audit-solution-term.kore audit-proof-term.kore
cmp_rc=$?
printf 'EXIT constructor_term_cmp=%s\n' "$cmp_rc"

printf '$ sha256sum audit-solution-term.kore audit-proof-term.kore\n'
sha256sum audit-solution-term.kore audit-proof-term.kore
sha_rc=$?
printf 'EXIT sha256sum=%s\n' "$sha_rc"

if (( solution_rc != 0 || proof_rc != 0 || cmp_rc != 0 || sha_rc != 0 )); then
  exit 1
fi
exit 0
