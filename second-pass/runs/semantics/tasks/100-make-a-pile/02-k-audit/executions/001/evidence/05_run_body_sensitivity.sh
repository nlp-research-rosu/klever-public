#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work
cp /audit-output/evidence/05_body_mutant_verification.k body-mutant-verification.k
cp /audit-output/evidence/05_body_mutant_spec.k body-mutant-spec.k

(
  echo 'COMMAND: kompile body-mutant-verification.k --backend haskell --main-module PILE-VERIFICATION-MUTANT --syntax-module MPY-SYNTAX --output-definition body-mutant-kompiled'
  kompile body-mutant-verification.k \
    --backend haskell \
    --main-module PILE-VERIFICATION-MUTANT \
    --syntax-module MPY-SYNTAX \
    --output-definition body-mutant-kompiled
  status=$?
  echo "EXIT_STATUS: ${status}"
  exit "${status}"
) > /audit-output/evidence/05a_body_mutant_kompile.log 2>&1
build_status=$?

(
  echo 'COMMAND: kprove body-mutant-spec.k --definition body-mutant-kompiled --spec-module PILE-BODY-MUTANT-SPEC'
  kprove body-mutant-spec.k \
    --definition body-mutant-kompiled \
    --spec-module PILE-BODY-MUTANT-SPEC
  status=$?
  echo "EXIT_STATUS: ${status}"
  exit "${status}"
) > /audit-output/evidence/05b_body_mutant_kprove.log 2>&1
prove_status=$?

echo "body_mutant_build_status=${build_status}"
echo "body_mutant_proof_status=${prove_status}"

if (( build_status != 0 )); then
  exit 1
fi
if (( prove_status == 0 )); then
  exit 2
fi
exit 0
