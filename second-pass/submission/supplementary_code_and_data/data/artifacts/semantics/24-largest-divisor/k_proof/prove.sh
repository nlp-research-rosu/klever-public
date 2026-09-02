#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and the concrete assertion program.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Mandated concrete LLVM definition and execution.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# Base symbolic definition: imports MPY, but never MPY-CONCRETE.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Every positive proof command below must print #Top and exit zero.
kprove spec.k --definition verification-kompiled --spec-module PREFIX-SPEC
kprove spec.k --definition verification-kompiled --spec-module INIT-SPEC
kprove spec.k --definition verification-kompiled --spec-module LOOP-SPEC
