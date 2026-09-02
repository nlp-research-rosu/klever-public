#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and the concrete assertion program.
python3 -c 'import ast; a=ast.parse(open("solution.py", encoding="utf-8").read()).body[0]; b=ast.parse(open("concrete-tests.py", encoding="utf-8").read()).body[0]; assert ast.dump(a, include_attributes=False) == ast.dump(b, include_attributes=False)'
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Required concrete LLVM definition and concrete program exercise.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  --warnings none
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty

# Symbolic definition and all positive target claims.
kompile verification.k \
  --backend haskell \
  --main-module CIRCULAR-SHIFT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  --warnings none
kprove \
  --definition verification-kompiled \
  --spec-module CIRCULAR-SHIFT-SPEC \
  --depth 300 \
  --warnings none \
  spec.k
