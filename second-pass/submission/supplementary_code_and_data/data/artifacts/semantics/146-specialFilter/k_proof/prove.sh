#!/usr/bin/env bash
set -euo pipefail

# Reproduce the required CPython-AST translation.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Required concrete LLVM definition and five assertion-based executions.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty | tee concrete-krun.out
grep -q "NoExc" concrete-krun.out

# Prove the universal, arbitrary-length loop claim directly from MPY.
kompile verification.k \
  --backend haskell \
  --main-module SPECIALFILTER-VERIFICATION-LOOP \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-kompiled
kprove spec.k \
  --definition loop-kompiled \
  --spec-module SPECIALFILTER-LOOP-SPEC | tee loop-proof.out
grep -qx "#Top" loop-proof.out

# Prove the closure-entry/return claim using the derived loop summary.
kompile verification.k \
  --backend haskell \
  --main-module SPECIALFILTER-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPECIALFILTER-SPEC | tee call-proof.out
grep -qx "#Top" call-proof.out
