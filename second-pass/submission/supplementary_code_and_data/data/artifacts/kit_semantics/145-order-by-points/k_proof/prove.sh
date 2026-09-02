#!/usr/bin/env bash
set -euo pipefail

mkdir -p proof-logs

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 validate.py 2>&1 | tee proof-logs/python-validation.out

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  2>&1 | tee proof-logs/llvm-kompile.out

krun concrete_tests.mpy \
  --definition runtime-kompiled \
  2>&1 | tee proof-logs/concrete-krun.out
rg -U -q '<exc>[[:space:]]+NoExc[[:space:]]+</exc>' \
  proof-logs/concrete-krun.out
rg -U -q '<exit-code>[[:space:]]+0[[:space:]]+</exit-code>' \
  proof-logs/concrete-krun.out

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  2>&1 | tee proof-logs/haskell-kompile.out

kast solution.mpy \
  --definition verification-kompiled \
  --module VERIFICATION-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  > solution.kore
kast \
  --expression solutionModule \
  --definition verification-kompiled \
  --module VERIFICATION-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  > verification-solution.kore
diff -u solution.kore verification-solution.kore \
  > proof-logs/program-identity.diff
echo "KORE program identity: identical" \
  | tee proof-logs/program-identity.out

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee proof-logs/kprove.out
rg -q '^#Top$' proof-logs/kprove.out

set +e
kprove mutation-spec.k \
  --definition verification-kompiled \
  --spec-module MUTATION-SPEC \
  --claims MUTATION-SPEC.digit-sum-body-mutation \
  > proof-logs/mutation-body.out 2>&1
mutation_body_status=$?
set -e
if [ "$mutation_body_status" -eq 0 ]; then
  echo "unexpected success: digit-sum body mutation" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' proof-logs/mutation-body.out
echo "digit-sum body mutation: expected exit $mutation_body_status" \
  | tee proof-logs/mutation-body-status.out

set +e
kprove mutation-spec.k \
  --definition verification-kompiled \
  --spec-module MUTATION-SPEC \
  --claims MUTATION-SPEC.target-postcondition-mutation \
  > proof-logs/mutation-postcondition.out 2>&1
mutation_postcondition_status=$?
set -e
if [ "$mutation_postcondition_status" -eq 0 ]; then
  echo "unexpected success: target postcondition mutation" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' proof-logs/mutation-postcondition.out
echo "target postcondition mutation: expected exit $mutation_postcondition_status" \
  | tee proof-logs/mutation-postcondition-status.out

echo "all positive proofs and validation checks passed"
