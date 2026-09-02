#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation, and ensure the concrete smoke
# program embeds that implementation verbatim.
python3 py2mpy.py solution.py > solution.mpy
head -n 7 concrete_tests.py | cmp - solution.py
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Concrete execution under the required LLVM definition.  A failed assertion
# sets the MPY exit code and makes krun exit nonzero.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Prove the inductive loop summary using only the supplied MPY semantics.
kompile verification.k \
  --backend haskell \
  --main-module X-OR-Y-VERIFICATION \
  --syntax-module X-OR-Y-VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module X-OR-Y-LOOP-SPEC \
  --claims loop_correct

# Import the now-proved summary as a modular proof rule, then prove the
# universal function contract.
kompile verification.k \
  --backend haskell \
  --main-module X-OR-Y-SUMMARY \
  --syntax-module X-OR-Y-SUMMARY \
  --output-definition summary-kompiled
kprove spec.k \
  --definition summary-kompiled \
  --spec-module X-OR-Y-MAIN-SPEC \
  --claims main_correct
