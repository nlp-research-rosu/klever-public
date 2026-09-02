#!/usr/bin/env bash
set -euo pipefail

# Regenerate the submitted constructor term and the concrete smoke program.
python3 py2mpy.py solution.py > solution.mpy
head -n 11 concrete-tests.py | cmp - solution.py
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Concrete execution uses the required LLVM main/syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# Symbolic verification imports MPY (not MPY-KRUN/MPY-CONCRETE).
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# First prove the structural loop invariant. Then prove the only remaining
# claim with that independently proved label available as a lemma.
kprove spec.k \
  --definition verification-kompiled \
  --claims loop-correct
kprove spec.k \
  --definition verification-kompiled \
  --trusted loop-correct
