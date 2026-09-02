#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and the concrete prompt examples.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Concrete execution uses exactly the required LLVM modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# First prove the finite typed-sequence bridge cases using only MPY plus the
# mathematical data representation (MAX-FILL-DATA contains no bridge rules).
kompile verification.k \
  --backend haskell \
  --main-module MAX-FILL-DATA \
  --syntax-module MPY-SYNTAX \
  --output-definition bridge-check-kompiled
kprove spec.k \
  --definition bridge-check-kompiled \
  --spec-module MAX-FILL-BRIDGE-SPEC

# Import those bridge cases and prove every unbounded functional-correctness
# claim together, so the outer loop can use the row-sum induction claim.
kompile verification.k \
  --backend haskell \
  --main-module MAX-FILL-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC
