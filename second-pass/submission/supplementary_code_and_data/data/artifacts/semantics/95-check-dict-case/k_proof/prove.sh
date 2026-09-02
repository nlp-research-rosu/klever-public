#!/usr/bin/env bash
set -euo pipefail

mkdir -p .build

# The required CPython-AST to K-constructor translation.
python3 py2mpy.py solution.py > solution.mpy
python3 - <<'PY'
import ast

with open("solution.py", encoding="utf-8") as stream:
    solution_function = ast.parse(stream.read()).body[0]
with open("smoke.py", encoding="utf-8") as stream:
    smoke_function = ast.parse(stream.read()).body[0]
assert ast.dump(solution_function) == ast.dump(smoke_function)
PY
python3 py2mpy.py smoke.py > .build/smoke.mpy

# Concrete LLVM execution using the required runtime main/syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition .build/runtime-kompiled
krun .build/smoke.mpy \
  --definition .build/runtime-kompiled \
  | tee .build/krun.out

# Symbolic definition imports MPY (and deliberately not MPY-CONCRETE).
kompile verification.k \
  --backend haskell \
  --main-module CHECK-DICT-CASE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition .build/verification-kompiled
kprove spec.k \
  --definition .build/verification-kompiled \
  --spec-module CHECK-DICT-CASE-SPEC \
  | tee .build/kprove.out

# Make the success witnesses explicit in the reproducible run.
rg -Uq '<exc>\s*NoExc\s*</exc>' .build/krun.out
rg -Uq '<exit-code>\s*0\s*</exit-code>' .build/krun.out
rg -qx '#Top' .build/kprove.out
