#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and the concrete assertion harness.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Concrete execution uses the required LLVM main/syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  --warnings none
krun concrete_tests.mpy --definition runtime-kompiled > concrete-run.out
grep -q "NoExc" concrete-run.out
if grep -q "AssertionError" concrete-run.out; then
  exit 1
fi

# The proof definition imports MPY (not the concrete-only MPY-KRUN module).
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  --warnings none

# First prove the universal recursive invariant. Then use that proved claim as
# a modular lemma while proving the public-entry claim and all concrete claims.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.all-balanced-inputs \
  --warnings none | tee proof-invariant.out
grep -qx "#Top" proof-invariant.out

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --trusted SPEC.all-balanced-inputs \
  --warnings none | tee proof-entry-and-examples.out
grep -qx "#Top" proof-entry-and-examples.out
