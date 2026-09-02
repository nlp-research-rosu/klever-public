#!/usr/bin/env bash
set -euo pipefail

# Generate the submitted program term and the concrete assertion harness.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

# Concrete execution uses exactly the supplied MPY-KRUN LLVM semantics.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

# Symbolic proofs import MPY (not MPY-KRUN/MPY-CONCRETE).
kompile verification.k \
  --backend haskell \
  --main-module SUM-TO-N-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SUM-TO-N-SPEC
