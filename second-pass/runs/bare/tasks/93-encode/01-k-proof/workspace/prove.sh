#!/usr/bin/env bash
set -euo pipefail

# Recreate the submitted constructor tree from the Python source.
python3 py2mpy.py solution.py > solution.mpy

# Abstract definition: keeps the exhaustively implemented character primitive
# opaque so the recursive loop invariant is a small induction proof.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Executable definition: supplies the ground character equations used by krun
# and by the concrete end-to-end proof claims.
kompile concrete-verification.k \
  --backend haskell \
  --main-module CONCRETE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-verification-kompiled

# Exercise the generated solution.mpy, including both examples in prompt.py.
krun solution.mpy \
  --definition concrete-verification-kompiled \
  -cMESSAGE='"test"'
krun solution.mpy \
  --definition concrete-verification-kompiled \
  -cMESSAGE='"This is a message"'

# Positive proof 1: universal recursive invariant for the exact translated
# loop body.  This must print #Top and exit 0.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.encode-loop-correct \
  --warnings none

# Positive proof 2: all concrete end-to-end claims (the two prompt examples
# and one exhaustive ASCII-letter/domain claim).  This must print #Top and
# exit 0.
kprove spec.k \
  --definition concrete-verification-kompiled \
  --spec-module CONCRETE-SPEC \
  --warnings none
