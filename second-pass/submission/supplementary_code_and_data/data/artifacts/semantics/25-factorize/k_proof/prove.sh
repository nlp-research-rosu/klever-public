#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# The concrete K harness contains the submitted source verbatim before its
# assertions; fail before testing if the two copies ever drift.
diff -u solution.py <(sed -n '1,13p' concrete_tests.py)
python3 py2mpy.py concrete_tests.py > concrete-tests.mpy

# Concrete LLVM execution, using the required modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled --output none
krun concrete-tests.mpy --definition runtime-kompiled --output none

# First prove the universal loop invariant directly against MPY.
kompile verification.k \
  --backend haskell \
  --main-module FACTORIZE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module FACTORIZE-LOOP-SPEC \
  --output pretty

# Then promote that exact proved claim to a priority proof lemma and prove the
# public entry-point theorem (initialization, call/return, and allocation).
kompile verification.k \
  --backend haskell \
  --main-module FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-with-lemma-kompiled
kprove spec.k \
  --definition verification-with-lemma-kompiled \
  --spec-module FACTORIZE-SPEC \
  --output pretty
