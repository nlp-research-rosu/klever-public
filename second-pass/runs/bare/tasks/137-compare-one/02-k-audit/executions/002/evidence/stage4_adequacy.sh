#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/137-compare-one-audit

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/claim_witnesses.py'
python3 /audit-output/evidence/claim_witnesses.py
status=$?
printf 'WITNESS SCRIPT EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'COMMAND: kompile verification-body-mutated.k --backend haskell --main-module VERIFICATION-BODY-MUTATED --syntax-module MPY-SYNTAX --output-definition body-mutation-kompiled'
kompile "$work/verification-body-mutated.k" \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUTATED \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/body-mutation-kompiled"
status=$?
printf 'BODY MUTATION BUILD EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'COMMAND: kast -e theSolutionBodyMutated --output kore > body-mutated-term.kore'
kast -e theSolutionBodyMutated \
  --definition "$work/body-mutation-kompiled" \
  --module VERIFICATION-BODY-MUTATED \
  --sort Pgm \
  --expand-macros \
  --output kore \
  > "$work/body-mutated-term.kore"
status=$?
printf 'BODY MUTATION KAST EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'COMMAND (expected different): cmp solution-term.kore body-mutated-term.kore'
cmp "$work/solution-term.kore" "$work/body-mutated-term.kore"
cmp_status=$?
printf 'BODY TERM CMP EXIT: %s\n' "$cmp_status"
if (( cmp_status == 0 )); then
  printf '%s\n' 'FAIL: body mutation did not change the executed program term'
  exit 1
fi

printf '%s\n' 'COMMAND (expected stuck claim): kprove spec-body-mutated.k --definition body-mutation-kompiled --spec-module SPEC-BODY-MUTATED --output pretty'
kprove "$work/spec-body-mutated.k" \
  --definition "$work/body-mutation-kompiled" \
  --spec-module SPEC-BODY-MUTATED \
  --output pretty
proof_status=$?
printf 'BODY MUTATION KPROVE EXIT: %s\n' "$proof_status"
if (( proof_status == 0 )); then
  printf '%s\n' 'FAIL: mutated body unexpectedly proves the original int-lt obligation'
  exit 1
fi

printf '%s\n' 'STAGE4_ADEQUACY_PROBES_COMPLETE'
