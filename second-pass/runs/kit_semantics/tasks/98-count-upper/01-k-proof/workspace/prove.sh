#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Translation and test-harness identity checks.
cmp solution.mpy <(python3 py2mpy.py solution.py)
echo "SOLUTION_TRANSLATION_MATCH=PASS"
cmp solution.py <(head -n 7 concrete_tests.py)
echo "CONCRETE_HARNESS_BODY_MATCH=PASS"
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 identity_test.py

# Independent CPython evidence.
python3 concrete_tests.py
echo "CPYTHON_CONCRETE_ASSERTS=5 PASS"
python3 differential_test.py

# Concrete execution under the supplied semantics.
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
echo "KRUN_SOLUTION_LOAD=PASS"
krun concrete_tests.mpy --definition runtime-kompiled
echo "KRUN_CONCRETE_ASSERTS=5 PASS"

# Symbolic proof under the supplied semantics plus verification.k.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
echo "KPROVE_LOOP_INVARIANT=PASS"
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
echo "KPROVE_ALL_CLAIMS=PASS"

# Gate A negative probes: both must be rejected.
if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
then
  echo "UNEXPECTED SUCCESS: false-result mutation proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: false-result mutation rejected"
fi

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
then
  echo "UNEXPECTED SUCCESS: mutated body proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: mutated body rejected"
fi
