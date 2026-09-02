#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

python3 - <<'PY'
import ast
import itertools
import random
from pathlib import Path

from solution import next_smallest


def first_function(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    return ast.dump(
        next(node for node in tree.body if isinstance(node, ast.FunctionDef)),
        include_attributes=False,
    )


def oracle(values):
    distinct = sorted(set(values))
    return distinct[1] if len(distinct) >= 2 else None


assert first_function("solution.py") == first_function("concrete_tests.py")
print("concrete harness function AST identity: PASS")

exhaustive_count = 0
for length in range(7):
    for values in itertools.product(range(-2, 3), repeat=length):
        values = list(values)
        assert next_smallest(values) == oracle(values)
        exhaustive_count += 1

rng = random.Random(20260731)
random_count = 10000
for _ in range(random_count):
    values = [rng.randint(-10**12, 10**12)
              for _ in range(rng.randint(0, 40))]
    assert next_smallest(values) == oracle(values)

print(
    "python differential: PASS "
    f"({exhaustive_count} exhaustive + {random_count} seeded random; "
    "mismatches=0)"
)
PY

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled > solution.krun.out
rg -Uq '<k>\s*\.K\s*</k>' solution.krun.out
rg -Uq '<exit-code>\s*0\s*</exit-code>' solution.krun.out
printf 'krun solution load: PASS\n'

krun concrete_tests.mpy --definition runtime-kompiled > concrete-tests.krun.out
rg -Uq '<k>\s*\.K\s*</k>' concrete-tests.krun.out
rg -Uq '<exc>\s*NoExc\s*</exc>' concrete-tests.krun.out
rg -Uq '<exit-code>\s*0\s*</exit-code>' concrete-tests.krun.out
printf 'krun concrete assertions: PASS\n'

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC | tee proof.out
rg -q '^#Top$' proof.out

kompile --backend haskell verification-mutation.k \
  --main-module MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-kompiled

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY > vacuity.out 2>&1
vacuity_status=$?

kprove spec-body-mutation.k \
  --definition mutation-kompiled \
  --spec-module SPEC-BODY-MUTATION > body-mutation.out 2>&1
body_status=$?
set -e

if [ "$vacuity_status" -eq 0 ] || ! rg -q 'WarnStuckClaimState' vacuity.out; then
  sed -n '1,180p' vacuity.out
  exit 1
fi

if [ "$body_status" -eq 0 ] || ! rg -q 'WarnStuckClaimState' body-mutation.out; then
  sed -n '1,180p' body-mutation.out
  exit 1
fi

printf 'vacuity mutation exit: %s (EXPECTED NONZERO)\n' "$vacuity_status"
printf 'body mutation exit: %s (EXPECTED NONZERO)\n' "$body_status"
rg -m1 'WarnStuckClaimState' vacuity.out
rg -m1 'WarnStuckClaimState' body-mutation.out
