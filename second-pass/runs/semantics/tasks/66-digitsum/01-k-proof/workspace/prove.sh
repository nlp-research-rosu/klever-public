#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and the concrete assertion suite.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Exercise the translated program with the required concrete LLVM semantics.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output pretty

# Prove the finite function initialization and the inductive loop theorem
# directly against the supplied MPY semantics.
kompile verification.k \
  --backend haskell \
  --main-module DIGIT-SUM-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module DIGIT-SUM-INITIALIZATION-SPEC \
  --output pretty
kprove spec.k \
  --definition verification-kompiled \
  --spec-module DIGIT-SUM-LOOP-SPEC \
  --output pretty

# Reuse those two proved claims as high-priority lemmas and prove their
# composition for the requested entry point.
kompile verification.k \
  --backend haskell \
  --main-module DIGIT-SUM-VERIFICATION-WITH-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-with-lemma-kompiled
kprove spec.k \
  --definition verification-with-lemma-kompiled \
  --spec-module DIGIT-SUM-ENTRY-SPEC \
  --output pretty
