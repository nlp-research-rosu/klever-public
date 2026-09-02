#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/31-is-prime-audit
cd "${work}" || exit 125
failures=0

echo 'MUTATION: verification-body-mutation.k changes the #entryBody final Return(Bool(true)) to Return(Bool(false)).'
echo 'This changes the macro term executed by entry-large-prefix; its explicit RHS remains the original submitted remainder.'
diff -u verification.k verification-body-mutation.k

echo 'COMMAND: kompile verification-body-mutation.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutation-kompiled'
timeout 900 kompile verification-body-mutation.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutation-kompiled
compile_status=$?
echo "EXIT_STATUS (compile): ${compile_status}"
if [[ ${compile_status} -ne 0 ]]; then failures=$((failures + 1)); fi

echo 'COMMAND: kast #entryBody from mutated definition'
kast --definition body-mutation-kompiled \
  --module VERIFICATION-BASE \
  --sort Stmts \
  --expression '#entryBody' \
  --expand-macros \
  --output json > entry-body.mutated.expanded.json
kast_status=$?
echo "EXIT_STATUS (kast): ${kast_status}"
if [[ ${kast_status} -ne 0 ]]; then failures=$((failures + 1)); fi

echo 'COMMAND: constructor comparison against submitted body (expected mismatch)'
python3 /audit-output/evidence/constructor_compare.py \
  solution.parsed.json \
  entry-body.mutated.expanded.json \
  prime-cond.expanded.json \
  prime-loop-body.expanded.json
compare_status=$?
echo "EXIT_STATUS (constructor comparison, expected 1): ${compare_status}"
if [[ ${compare_status} -eq 0 ]]; then failures=$((failures + 1)); fi

echo 'COMMAND: kprove mutated entry-large-prefix claim (expected proof failure)'
timeout 900 kprove spec-body-mutation.k \
  --definition body-mutation-kompiled \
  --spec-module SPEC \
  --claims entry-large-prefix
prove_status=$?
echo "EXIT_STATUS (proof, expected nonzero): ${prove_status}"
if [[ ${prove_status} -eq 0 ]]; then failures=$((failures + 1)); fi

echo "EXPECTED_FAILURES_OBSERVED: constructor_status=${compare_status} proof_status=${prove_status}"
echo "FAILURE_COUNT: ${failures}"
if [[ ${failures} -ne 0 ]]; then exit 1; fi
exit 0
