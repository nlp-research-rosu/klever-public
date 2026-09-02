#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/130-tri-audit
source_root=/audit-output/evidence
cd "$audit_work" || exit 2

printf 'COMMAND: copy reviewer-authored body mutation to scratch\n'
cp -p \
  "$source_root/verification-body-mutant.k" \
  "$source_root/body-mutant-spec.k" \
  "$audit_work/"
copy_status=$?
printf 'COPY_EXIT_STATUS=%s\n' "$copy_status"

printf 'COMMAND: kompile body-mutated definition\n'
kompile verification-body-mutant.k \
  --backend haskell \
  --main-module TRI-VERIFICATION-BODY-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutant-kompiled
build_status=$?
printf 'BUILD_EXIT_STATUS=%s\n' "$build_status"
if [[ "$build_status" -ne 0 ]]; then
  exit "$build_status"
fi

printf 'COMMAND: kast expanded materially mutated program term\n'
kast --definition body-mutant-kompiled \
  --module TRI-VERIFICATION-BODY-MUTANT \
  --sort Program \
  --expand-macros \
  --output kore \
  --expression mutatedSolutionProgram > mutated-program.kore
mutant_kast_status=$?
printf 'MUTANT_KAST_EXIT_STATUS=%s\n' "$mutant_kast_status"

printf 'COMMAND: cmp -s submitted-program.kore mutated-program.kore\n'
cmp -s submitted-program.kore mutated-program.kore
body_term_cmp_status=$?
printf 'EXPECTED_DIFFERENT_PROGRAM_TERM_CMP_EXIT_STATUS=%s\n' \
  "$body_term_cmp_status"
sha256sum submitted-program.kore mutated-program.kore

printf 'COMMAND: kprove false result for the mutated executed body\n'
kprove body-mutant-spec.k \
  --definition body-mutant-kompiled \
  --spec-module BODY-MUTANT-SPEC
prove_status=$?
printf 'EXPECTED_BODY_MUTATION_PROOF_FAILURE_EXIT_STATUS=%s\n' "$prove_status"

if [[ "$copy_status" -ne 0 || "$mutant_kast_status" -ne 0 ]]; then
  exit 1
fi
if [[ "$body_term_cmp_status" -eq 0 ]]; then
  printf 'ERROR: body mutation did not change the executed program term\n' >&2
  exit 1
fi
if [[ "$prove_status" -eq 0 ]]; then
  printf 'ERROR: materially false body mutation unexpectedly proved\n' >&2
  exit 1
fi

printf 'BODY_SENSITIVITY_PASS\n'
