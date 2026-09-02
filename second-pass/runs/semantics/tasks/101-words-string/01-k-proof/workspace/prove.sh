#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and ensure the concrete harness uses
# the same function definition.
python3 py2mpy.py solution.py > solution.mpy
cmp solution.py <(sed -n '1,2p' concrete_tests.py)
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Required concrete LLVM definition and executions.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled --output none
krun concrete_tests.mpy --definition runtime-kompiled --output none

# Symbolic definition and the universal contract proof.
kompile verification.k \
  --backend haskell \
  --main-module WORDS-STRING-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module WORDS-STRING-SPEC \
  2>&1 | tee kprove.out
grep -qx '#Top' kprove.out
