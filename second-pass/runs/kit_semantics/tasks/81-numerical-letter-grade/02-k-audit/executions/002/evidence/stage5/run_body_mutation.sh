#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate-src || exit 90

printf '$ kompile /audit-output/evidence/stage5/body-mutant-verification.k --backend haskell --main-module BODY-MUTANT-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-body-mutant-kompiled\n'
kompile /audit-output/evidence/stage5/body-mutant-verification.k \
  --backend haskell \
  --main-module BODY-MUTANT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-body-mutant-kompiled
compile_rc=$?
printf 'EXIT compile=%s\n' "$compile_rc"
if (( compile_rc != 0 )); then
  exit 1
fi

printf '$ kast --definition audit-body-mutant-kompiled --module BODY-MUTANT-VERIFICATION --sort Module --expand-macros --output kore --expression MUTANT-PROGRAM > audit-mutant-term.kore\n'
kast --definition audit-body-mutant-kompiled \
  --module BODY-MUTANT-VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  --expression 'MUTANT-PROGRAM' > audit-mutant-term.kore
kast_rc=$?
printf 'EXIT kast_mutant=%s\n' "$kast_rc"

printf '$ cmp -s audit-mutant-term.kore audit-solution-term.kore\n'
cmp -s audit-mutant-term.kore audit-solution-term.kore
term_cmp_rc=$?
printf 'EXIT mutant_differs_from_submitted=%s expected=1\n' "$term_cmp_rc"

printf '$ kprove /audit-output/evidence/stage5/spec-entry-body-mutation.k --definition audit-body-mutant-kompiled --spec-module SPEC-ENTRY-BODY-MUTATION\n'
kprove /audit-output/evidence/stage5/spec-entry-body-mutation.k \
  --definition audit-body-mutant-kompiled \
  --spec-module SPEC-ENTRY-BODY-MUTATION
proof_rc=$?
printf 'EXIT mutated_entry_proof=%s expected_nonzero=1\n' "$proof_rc"

if (( kast_rc != 0 || term_cmp_rc == 0 || proof_rc == 0 )); then
  exit 1
fi
exit 0
