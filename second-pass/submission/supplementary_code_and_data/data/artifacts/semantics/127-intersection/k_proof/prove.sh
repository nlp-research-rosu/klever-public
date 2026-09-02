#!/usr/bin/env bash
set -euo pipefail

# Regenerate every translated artifact from its Python source.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Ensure the concrete harness executes exactly the delivered implementation.
python3 - <<'PY'
import ast
from pathlib import Path

solution_tree = ast.parse(Path("solution.py").read_text())
tests_tree = ast.parse(Path("concrete-tests.py").read_text())
assert ast.dump(solution_tree.body[0]) == ast.dump(tests_tree.body[0])
PY

# Concrete execution uses the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty

# First prove the recursive loop invariant directly against the supplied MPY
# semantics plus proof-only mathematical definitions.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC \
  --claims loop-correct \
  --output pretty

# Then install precisely that proved invariant as a modular summary and prove
# the universally quantified end-to-end function contract.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims intersection-correct \
  --output pretty
