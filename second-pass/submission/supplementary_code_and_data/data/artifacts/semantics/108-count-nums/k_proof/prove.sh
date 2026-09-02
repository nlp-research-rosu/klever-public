#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution using the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy --definition runtime-kompiled

# Prove each layer only after compiling the previously proved lemmas.
# In particular, the definition used for a claim never contains that claim's
# own summary rule.
kompile verification.k \
  --backend haskell \
  --main-module COUNT-NUMS-VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-base-kompiled
kprove spec.k \
  --definition loop-base-kompiled \
  --spec-module POSITIVE-LOOP-SPEC
kprove spec.k \
  --definition loop-base-kompiled \
  --spec-module NEGATIVE-LOOP-SPEC

kompile verification.k \
  --backend haskell \
  --main-module DIGIT-LOOP-LEMMAS \
  --syntax-module MPY-SYNTAX \
  --output-definition digit-loop-kompiled
kprove spec.k \
  --definition digit-loop-kompiled \
  --spec-module POSITIVE-FUNCTION-SPEC
kprove spec.k \
  --definition digit-loop-kompiled \
  --spec-module NEGATIVE-FUNCTION-SPEC

kompile verification.k \
  --backend haskell \
  --main-module DIGIT-FUNCTION-LEMMAS \
  --syntax-module MPY-SYNTAX \
  --output-definition digit-function-kompiled
kprove spec.k \
  --definition digit-function-kompiled \
  --spec-module SIGNED-FUNCTION-SPEC

kompile verification.k \
  --backend haskell \
  --main-module SIGNED-DIGIT-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition signed-digit-kompiled
kprove spec.k \
  --definition signed-digit-kompiled \
  --spec-module COUNT-LOOP-WITH-N-SPEC

kompile verification.k \
  --backend haskell \
  --main-module COUNT-LOOP-WITH-N-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition count-loop-with-n-kompiled
kprove spec.k \
  --definition count-loop-with-n-kompiled \
  --spec-module COUNT-LOOP-SPEC

kompile verification.k \
  --backend haskell \
  --main-module COUNT-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition count-loop-kompiled
kprove spec.k \
  --definition count-loop-kompiled \
  --spec-module COUNT-NUMS-SPEC
