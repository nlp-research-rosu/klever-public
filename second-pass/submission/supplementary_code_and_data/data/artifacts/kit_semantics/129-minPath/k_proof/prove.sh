#!/usr/bin/env bash
set -eu

# Recreate the translated program from the preserved Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution uses the supplied semantics without proof extensions.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  -o runtime-kompiled
krun smoke_odd.mpy --definition runtime-kompiled
krun smoke_even.mpy --definition runtime-kompiled

# Symbolic definition and the independently closing auxiliary claims.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  -o verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-one-ahead,SPEC.inner-no-one,SPEC.outer-one-ahead,SPEC.outer-one-past,SPEC.scan-finish \
  --depth 240
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.neighbor-finish \
  --depth 400
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.result-loop-tail \
  --depth 110

# Required positive full-contract target.  At handoff this command is expected
# to exit nonzero with the residual documented in NOTES.md and PROOF.md.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.scan-finish,SPEC.neighbor-finish,SPEC.result-loop-tail,SPEC.minpath-full-contract \
  --trusted SPEC.scan-finish,SPEC.neighbor-finish,SPEC.result-loop-tail \
  --depth 240
