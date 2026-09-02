#!/usr/bin/env bash
set +e
scratch=/tmp/audit-work/92-any-int-audit
evidence=/audit-output/evidence

printf '$ kast solution.mpy --definition audit-verification-kompiled --module VERIFICATION-SYNTAX --sort Module --expand-macros --output json > solution-kast.json\n'
(
  cd "$scratch" || exit 125
  kast solution.mpy \
    --definition audit-verification-kompiled \
    --module VERIFICATION-SYNTAX \
    --sort Module \
    --expand-macros \
    --output json > solution-kast.json
)
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ kast --expression anyIntModuleScope --definition audit-verification-kompiled --module VERIFICATION-SYNTAX --sort Scope --expand-macros --output json > scope-kast.json\n'
(
  cd "$scratch" || exit 125
  kast --expression 'anyIntModuleScope' \
    --definition audit-verification-kompiled \
    --module VERIFICATION-SYNTAX \
    --sort Scope \
    --expand-macros \
    --output json > scope-kast.json
)
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ kast --expression "AnyIntCall(5, 2, 7)" --definition audit-verification-kompiled --module VERIFICATION-SYNTAX --sort Expr --expand-macros --output json > call-kast.json\n'
(
  cd "$scratch" || exit 125
  kast --expression 'AnyIntCall(5, 2, 7)' \
    --definition audit-verification-kompiled \
    --module VERIFICATION-SYNTAX \
    --sort Expr \
    --expand-macros \
    --output json > call-kast.json
)
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ python3 /audit-output/evidence/04_compare_terms.py\n'
python3 "$evidence/04_compare_terms.py"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ python3 /audit-output/evidence/04_witnesses.py\n'
python3 "$evidence/04_witnesses.py"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ cp /audit-output/evidence/04_verification_body_mutant.k /audit-output/evidence/04_spec_body_mutant.k /tmp/audit-work/92-any-int-audit/\n'
cp "$evidence/04_verification_body_mutant.k" "$evidence/04_spec_body_mutant.k" "$scratch/"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ kompile --backend haskell 04_verification_body_mutant.k --main-module AUDIT-BODY-MUTANT --syntax-module MPY-SYNTAX --output-definition audit-body-mutant-kompiled\n'
(
  cd "$scratch" || exit 125
  kompile --backend haskell 04_verification_body_mutant.k \
    --main-module AUDIT-BODY-MUTANT \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-body-mutant-kompiled
) > "$evidence/04_body_mutant_kompile.log" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
tail -n 120 "$evidence/04_body_mutant_kompile.log"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

printf '$ kprove 04_spec_body_mutant.k --definition audit-body-mutant-kompiled --spec-module AUDIT-BODY-MUTANT-SPEC\n'
(
  cd "$scratch" || exit 125
  kprove 04_spec_body_mutant.k \
    --definition audit-body-mutant-kompiled \
    --spec-module AUDIT-BODY-MUTANT-SPEC
) > "$evidence/04_body_mutant_kprove.log" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
tail -n 180 "$evidence/04_body_mutant_kprove.log"
if [ "$status" -eq 0 ]; then
  printf 'BODY_MUTATION_RESULT: UNEXPECTED_PROOF_SUCCESS\n'
  exit 1
fi
if grep -q 'WarnStuckClaimState' "$evidence/04_body_mutant_kprove.log" &&
   grep -q '<k>' "$evidence/04_body_mutant_kprove.log" &&
   grep -q 'false' "$evidence/04_body_mutant_kprove.log"; then
  printf 'BODY_MUTATION_RESULT: EXPECTED_STUCK_FALSE_RESULT\n'
  exit 0
fi
printf 'BODY_MUTATION_RESULT: WRONG_FAILURE_MODE\n'
exit 1
