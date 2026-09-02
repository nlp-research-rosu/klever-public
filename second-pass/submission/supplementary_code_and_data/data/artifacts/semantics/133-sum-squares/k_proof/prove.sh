#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and the concrete smoke program.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Concrete execution uses the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output pretty

# First prove the inductive loop lemma without assuming its promoted rule.
kompile verification.k \
  --backend haskell \
  --main-module SUM-SQUARES-VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-verification-kompiled
kprove spec.k \
  --definition loop-verification-kompiled \
  --spec-module SUM-SQUARES-LOOP-SPEC \
  --claims SUM-SQUARES-LOOP-SPEC.loop-correct \
  --output pretty

# Then make the proved loop lemma available to the end-to-end call proof.
kompile verification.k \
  --backend haskell \
  --main-module SUM-SQUARES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SUM-SQUARES-SPEC \
  --claims SUM-SQUARES-SPEC.function-correct \
  --output pretty
