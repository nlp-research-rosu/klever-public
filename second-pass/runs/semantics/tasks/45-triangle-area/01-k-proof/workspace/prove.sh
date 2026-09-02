#!/usr/bin/env bash
set -euo pipefail

# Recreate both constructor programs with the fixed translator.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

# Compile and exercise the supplied concrete semantics.  All four assertions in
# smoke.mpy must terminate with NoExc and exit code 0.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

# Compile the proof definition without the concrete-only MPY-KRUN extension,
# then prove every claim in spec.k.
kompile verification.k \
  --backend haskell \
  --main-module TRIANGLE-AREA-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module TRIANGLE-AREA-SPEC
