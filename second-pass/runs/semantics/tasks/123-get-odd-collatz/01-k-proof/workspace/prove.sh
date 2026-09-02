#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and the concrete assertion harness.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 -c 'import ast; s=ast.parse(open("solution.py", encoding="utf-8").read()); t=ast.parse(open("concrete_tests.py", encoding="utf-8").read()); assert ast.dump(s.body[0], include_attributes=False) == ast.dump(t.body[0], include_attributes=False)'

# Required concrete LLVM definition and representative executions.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output none

# Symbolic definition and all positive proof claims.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --depth 2000 \
  --smt-timeout 5000
