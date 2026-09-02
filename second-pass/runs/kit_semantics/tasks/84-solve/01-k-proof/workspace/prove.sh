#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

cmp -s \
  solution.mpy \
  <(sed -n '/BEGIN SOLUTION MPY/,/END SOLUTION MPY/p' verification.k \
      | sed '1d;$d;s/^    //')
echo "program-identity-check: PASS"

python3 test_solution.py | tee python-evidence.log

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  2>&1 | tee llvm-compile.log

krun \
  <(sed '$a\
assert solve(1000) == "1"\
assert solve(150) == "110"\
assert solve(147) == "1100"\
assert solve(0) == "0"\
assert solve(9999) == "100100"' solution.py \
    | python3 py2mpy.py /dev/stdin) \
  --definition runtime-kompiled \
  > concrete.log
rg -q '^    \.K$' concrete.log
rg -q '^    NoExc$' concrete.log
echo "krun-example-check: PASS"

kompile --backend haskell bridge-verification.k \
  --main-module BRIDGE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition bridge-verification-kompiled \
  2>&1 | tee bridge-kompile.log

kprove bridge-spec.k \
  --definition bridge-verification-kompiled \
  --spec-module BRIDGE-SPEC \
  2>&1 | tee bridge-proof.log
rg -q '^#Top$' bridge-proof.log

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  2>&1 | tee verification-kompile.log

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee target-proof.log
rg -q '^#Top$' target-proof.log

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > vacuity.log 2>&1
vacuity_rc=$?
set -e
if [[ $vacuity_rc -eq 0 ]]; then
  echo "false-postcondition probe unexpectedly passed" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' vacuity.log
echo "false-postcondition-check: EXPECTED FAILURE (exit $vacuity_rc)"

set +e
kprove bridge-negative-spec.k \
  --definition bridge-verification-kompiled \
  --spec-module BRIDGE-NEGATIVE-SPEC \
  --claims BRIDGE-NEGATIVE-SPEC.wrong-mod \
  > bridge-wrong-mod.log 2>&1
wrong_mod_rc=$?
kprove bridge-negative-spec.k \
  --definition bridge-verification-kompiled \
  --spec-module BRIDGE-NEGATIVE-SPEC \
  --claims BRIDGE-NEGATIVE-SPEC.wrong-floordiv \
  > bridge-wrong-floordiv.log 2>&1
wrong_div_rc=$?
set -e
if [[ $wrong_mod_rc -eq 0 || $wrong_div_rc -eq 0 ]]; then
  echo "opposite arithmetic-value probe unexpectedly passed" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' bridge-wrong-mod.log
rg -q 'WarnStuckClaimState' bridge-wrong-floordiv.log
echo "wrong-arithmetic-value-checks: EXPECTED FAILURE (exits $wrong_mod_rc, $wrong_div_rc)"

sed '0,/Return(Str("110"))/s//Return(Str("111"))/' \
  verification.k > verification-mutant.k
sed 's/requires "verification.k"/requires "verification-mutant.k"/' \
  spec.k > spec-mutant.k

kompile --backend haskell verification-mutant.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-mutant-kompiled \
  2>&1 | tee mutation-kompile.log

set +e
kprove spec-mutant.k \
  --definition verification-mutant-kompiled \
  --spec-module SPEC \
  --claims SPEC.solve-sum-00-07 \
  > body-mutation.log 2>&1
body_mutation_rc=$?
set -e
if [[ $body_mutation_rc -eq 0 ]]; then
  echo "body-sensitivity mutation unexpectedly passed" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' body-mutation.log
echo "body-sensitivity-check: EXPECTED FAILURE (exit $body_mutation_rc)"

echo "all positive proofs and validation probes behaved as required"
