#!/usr/bin/env bash
set -euo pipefail

# Recreate the required transliteration from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Compile exactly the supplied concrete semantics and run executable assertions.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy --definition runtime-kompiled | tee concrete-krun.out

# Prove the loop summary without assuming that summary.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC \
  --claims LOOP-SPEC.loop-invariant | tee loop-proof.out
rg -Fx '#Top' loop-proof.out

# Compile the compositional verifier and prove the whole translated body.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.function-correct | tee function-proof.out
rg -Fx '#Top' function-proof.out
