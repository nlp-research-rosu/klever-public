#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/maximum-120-audit
EVIDENCE=/audit-output/evidence
status=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then status=1; fi
}

printf 'Parse and macro-expand the submitted module and claimed function body:\n'
printf '\n$ kast --definition %s/verification-kompiled --module MAXIMUM-VERIFICATION --sort Module --expand-macros --output json /candidate/solution.mpy > %s/solution-expanded-kast.json\n' "$WORK" "$EVIDENCE"
kast --definition "$WORK/verification-kompiled" \
  --module MAXIMUM-VERIFICATION \
  --sort Module \
  --expand-macros \
  --output json \
  /candidate/solution.mpy > "$EVIDENCE/solution-expanded-kast.json"
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi

printf '\n$ kast --definition %s/verification-kompiled --module MAXIMUM-VERIFICATION --sort Stmts --expression maximumBody --expand-macros --output json > %s/maximumBody-expanded-kast.json\n' "$WORK" "$EVIDENCE"
kast --definition "$WORK/verification-kompiled" \
  --module MAXIMUM-VERIFICATION \
  --sort Stmts \
  --expression maximumBody \
  --expand-macros \
  --output json > "$EVIDENCE/maximumBody-expanded-kast.json"
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi

run python3 "$EVIDENCE/compare_constructor_terms.py"

printf '\nGround substitutions for the formal RHS and both Python implementations:\n'
run kompile "$WORK/post-eval.k" \
  --backend haskell \
  --main-module POST-EVAL \
  --syntax-module MPY-SYNTAX \
  --output-definition "$WORK/post-eval-haskell-kompiled"
run kprove "$WORK/post-eval-spec.k" \
  --definition "$WORK/post-eval-haskell-kompiled" \
  --spec-module POST-EVAL-SPEC
run python3 "$EVIDENCE/witness_outputs.py"

printf '\nBody-sensitivity mutation definition:\n'
run kompile "$WORK/verification-body-mutated.k" \
  --backend haskell \
  --main-module MAXIMUM-BODY-MUTATED \
  --syntax-module MPY-SYNTAX \
  --output-definition "$WORK/body-mutated-kompiled"

printf '\nExpected failure: the result claim must reject the changed executed body.\n'
printf '$ kprove %q --definition %q --spec-module SPEC-BODY-MUTATED\n' \
  "$WORK/spec-body-mutated.k" "$WORK/body-mutated-kompiled"
kprove "$WORK/spec-body-mutated.k" \
  --definition "$WORK/body-mutated-kompiled" \
  --spec-module SPEC-BODY-MUTATED
rc=$?
printf '[exit %d; expected nonzero]\n' "$rc"
if (( rc == 0 )); then
  printf 'ERROR: body mutation unexpectedly proved\n'
  status=1
fi

exit "$status"
