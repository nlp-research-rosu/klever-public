#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy \
  --definition runtime-kompiled \
  --output pretty

krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  -I . \
  --output-definition verification-kompiled

# Prove the reusable loop invariant independently.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-correct \
  --output pretty

# Use the independently proved invariant as the loop lemma for the entry
# theorem.  Both labels must remain selected so the claim is available.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-correct,SPEC.sort-even-correct \
  --trusted SPEC.loop-correct \
  --output pretty
