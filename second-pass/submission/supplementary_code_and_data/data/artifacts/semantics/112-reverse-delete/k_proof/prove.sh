#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# Ensure the concrete harness embeds exactly the submitted function.
cmp solution.py <(head -n 9 concrete_tests.py)
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Concrete execution uses the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Symbolic verification imports MPY through verification.k.
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# First prove the loop summary without importing the summary rule.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module LOOP-SPEC

# Then use that proved summary to close the exact function-body claim.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
