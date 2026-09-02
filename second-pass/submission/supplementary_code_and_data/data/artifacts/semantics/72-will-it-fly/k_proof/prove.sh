#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# Ensure the concrete test harness embeds the submitted entry point verbatim.
python3 - <<'PY'
import ast

with open("solution.py", encoding="utf-8") as stream:
    solution = ast.parse(stream.read())
with open("concrete-tests.py", encoding="utf-8") as stream:
    tests = ast.parse(stream.read())

assert ast.dump(solution.body[0], include_attributes=False) == ast.dump(
    tests.body[0], include_attributes=False
)
PY

# Compile and exercise the supplied concrete semantics.
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# Compile the symbolic definition and prove all contract claims.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
