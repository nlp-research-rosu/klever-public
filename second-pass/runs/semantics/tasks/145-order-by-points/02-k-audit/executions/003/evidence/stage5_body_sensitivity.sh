#!/usr/bin/env bash
set -u
cd /tmp/audit-work/source

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/make_body_mutation.py > verification-body-mutated.k'
python3 /audit-output/evidence/make_body_mutation.py \
  > verification-body-mutated.k
printf 'MUTATION_EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: kompile verification-body-mutated.k --backend haskell --main-module ORDER-BY-POINTS-VERIFICATION-BODY-MUTATED --syntax-module MPY-SYNTAX --output-definition body-mutated-kompiled'
kompile \
  verification-body-mutated.k \
  --backend haskell \
  --main-module ORDER-BY-POINTS-VERIFICATION-BODY-MUTATED \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutated-kompiled
printf 'BUILD_EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: rg -n -F #token("999","Int") body-mutated-kompiled/compiled.txt'
rg -n -F '#token("999","Int")' body-mutated-kompiled/compiled.txt
printf 'MUTATED_TERM_CHECK_EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: kprove spec-body-mutated.k --definition body-mutated-kompiled --spec-module REVIEWER-SPEC-BODY-MUTATED --claims order_after_body_mutation'
kprove \
  spec-body-mutated.k \
  --definition body-mutated-kompiled \
  --spec-module REVIEWER-SPEC-BODY-MUTATED \
  --claims order_after_body_mutation
printf 'PROOF_EXIT_STATUS: %s\n' "$?"
