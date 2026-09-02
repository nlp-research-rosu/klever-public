#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# Ensure the concrete harness embeds exactly the submitted function, then
# translate it for execution by the supplied LLVM semantics.
python3 - <<'PY'
import ast

with open("solution.py", encoding="utf-8") as solution_file:
    solution_tree = ast.parse(solution_file.read())
with open("smoke.py", encoding="utf-8") as smoke_file:
    smoke_tree = ast.parse(smoke_file.read())

assert ast.dump(solution_tree.body[0]) == ast.dump(smoke_tree.body[0])
PY
python3 py2mpy.py smoke.py > smoke.mpy

# Concrete execution uses the required concrete main module.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy \
  --definition runtime-kompiled \
  --output pretty

# Symbolic verification imports MPY (not MPY-KRUN/MPY-CONCRETE).
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
