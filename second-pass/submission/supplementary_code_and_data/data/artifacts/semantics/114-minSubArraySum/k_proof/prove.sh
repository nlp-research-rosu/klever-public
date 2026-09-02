#!/usr/bin/env bash
set -euo pipefail

# Regenerate the required constructor term from the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# Check that the concrete harness contains the identical function AST, then
# translate it.  Only the harness's top-level assertions differ.
python3 - <<'PY'
import ast
from pathlib import Path

solution = ast.parse(Path("solution.py").read_text(encoding="utf-8"))
harness = ast.parse(Path("concrete-tests.py").read_text(encoding="utf-8"))
assert ast.dump(solution.body[0]) == ast.dump(harness.body[0])
PY
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Concrete execution uses the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty

# Prove the inductive loop theorem and the exact definition-loading claim
# without making the loop summary rule available.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC \
  --output pretty
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module LOAD-SPEC \
  --output pretty

# Compile the proved loop theorem as a summary, then prove the full generated
# closure correct for every non-empty integer sequence.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module FUNCTION-SPEC \
  --output pretty
