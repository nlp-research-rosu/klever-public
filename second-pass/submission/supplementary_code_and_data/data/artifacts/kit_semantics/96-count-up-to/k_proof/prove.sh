#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

python3 - <<'PY'
from solution import count_up_to

cases = {
    5: [2, 3],
    11: [2, 3, 5, 7],
    0: [],
    20: [2, 3, 5, 7, 11, 13, 17, 19],
    1: [],
    18: [2, 3, 5, 7, 11, 13, 17],
}
for bound, expected in cases.items():
    assert count_up_to(bound) == expected
print(f"CPython examples: {len(cases)} passed")
PY

python3 differential_test.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 - <<'PY'
import ast

def first_function(path):
    tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    return ast.dump(
        next(node for node in tree.body if isinstance(node, ast.FunctionDef)),
        include_attributes=False,
    )

assert first_function("solution.py") == first_function("smoke.py")
print("smoke function AST matches solution.py")
PY

python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kast --definition verification-kompiled \
  --module VERIFICATION-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  --expression 'Module(FuncDef("count_up_to", Params("n"), countBody))' \
  > /tmp/count-up-to-proof-program.kore
kast --definition verification-kompiled \
  --module MPY-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  solution.mpy \
  > /tmp/count-up-to-solution-program.kore
cmp /tmp/count-up-to-proof-program.kore \
    /tmp/count-up-to-solution-program.kore
sha256sum /tmp/count-up-to-proof-program.kore \
          /tmp/count-up-to-solution-program.kore

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
vacuity_rc=$?
echo "VACUITY_EXPECTED_NONZERO_RC=$vacuity_rc"

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
body_mutation_rc=$?
echo "BODY_MUTATION_EXPECTED_NONZERO_RC=$body_mutation_rc"

kprove spec-value-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-VALUE-MUTATION-PRIME
prime_value_rc=$?
echo "PRIME_VALUE_EXPECTED_NONZERO_RC=$prime_value_rc"

kprove spec-value-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-VALUE-MUTATION-COMPOSITE
composite_value_rc=$?
echo "COMPOSITE_VALUE_EXPECTED_NONZERO_RC=$composite_value_rc"
set -e

test "$vacuity_rc" -ne 0
test "$body_mutation_rc" -ne 0
test "$prime_value_rc" -ne 0
test "$composite_value_rc" -ne 0
