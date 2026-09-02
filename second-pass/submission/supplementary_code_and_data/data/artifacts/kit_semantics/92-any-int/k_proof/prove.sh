#!/usr/bin/env bash
set -eu

# Recreate the translated deliverable from the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution under the required LLVM main module.
python3 - <<'PY'
import ast

with open("solution.py", encoding="utf-8") as source_file:
    solution_tree = ast.parse(source_file.read())
with open("concrete_tests.py", encoding="utf-8") as tests_file:
    tests_tree = ast.parse(tests_file.read())

solution_function = next(
    node for node in solution_tree.body if isinstance(node, ast.FunctionDef)
)
tests_function = next(
    node for node in tests_tree.body if isinstance(node, ast.FunctionDef)
)
if ast.dump(solution_function) != ast.dump(tests_function):
    raise SystemExit("concrete test function differs from solution.py")
print("program-identity=match")
PY
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Required symbolic target proof: every claim in SPEC is selected.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Independent finite differential evidence.
python3 differential_test.py

# Gate A5: the deliberately false postcondition must be rejected.
if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY; then
  echo "ERROR: false-postcondition probe unexpectedly proved"
  exit 1
else
  status=$?
  echo "EXPECTED FAILURE: false-postcondition probe exited ${status}"
fi

# Gate A1: a material body mutation must invalidate its witness.
kompile --backend haskell verification-mutant.k \
  --main-module VERIFICATION-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition mutant-kompiled
if kprove spec-mutant.k \
    --definition mutant-kompiled \
    --spec-module SPEC-MUTANT; then
  echo "ERROR: body-mutation probe unexpectedly proved"
  exit 1
else
  status=$?
  echo "EXPECTED FAILURE: body-mutation probe exited ${status}"
fi
