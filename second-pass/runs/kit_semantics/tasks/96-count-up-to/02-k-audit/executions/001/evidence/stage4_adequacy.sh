#!/usr/bin/env bash
set -euo pipefail
export PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

python3 /audit-output/evidence/stage4_ground_witnesses.py
echo "GROUND_WITNESSES_EXIT=$?"

cd /tmp/audit-work/reconstruction

kast --definition reviewer-verification-kompiled \
  --module VERIFICATION-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  --expression 'Module(FuncDef("count_up_to", Params("n"), countBodyStart3))' \
  > reviewer-mutated-program.kore
echo "MUTATED_PROGRAM_KAST_EXIT=$?"

sha256sum reviewer-mutated-program.kore reviewer-solution-program.kore

set +e
cmp reviewer-mutated-program.kore reviewer-solution-program.kore
mutated_cmp_rc=$?
set -e
echo "BODY_MUTATION_TERM_DIFFERENCE_EXPECTED_NONZERO_EXIT=$mutated_cmp_rc"
test "$mutated_cmp_rc" -ne 0

set +e
timeout 600 kprove spec-body-mutation.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
body_proof_rc=$?
set -e
echo "BODY_MUTATION_PROOF_EXPECTED_NONZERO_EXIT=$body_proof_rc"
test "$body_proof_rc" -ne 0
