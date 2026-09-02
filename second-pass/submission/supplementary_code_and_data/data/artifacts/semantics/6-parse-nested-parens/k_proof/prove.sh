#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# Build and run concrete assertions through the required LLVM semantics.
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 - <<'PY'
import ast

with open('solution.py', encoding='utf-8') as stream:
    solution_module = ast.parse(stream.read())
with open('concrete_tests.py', encoding='utf-8') as stream:
    concrete_module = ast.parse(stream.read())

solution_function = solution_module.body[1]
concrete_function = concrete_module.body[1]
assert ast.dump(solution_function, include_attributes=False) == ast.dump(
    concrete_function, include_attributes=False
)
PY
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled --output none

# Build the symbolic definition, then prove every claim together so the
# target theorem can use the independently proved loop invariant.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
