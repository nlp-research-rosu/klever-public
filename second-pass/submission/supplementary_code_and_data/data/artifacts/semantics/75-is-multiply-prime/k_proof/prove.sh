#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# Required concrete LLVM definition and representative end-to-end execution.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled

# The proof definition imports MPY (not its concrete-only MPY-KRUN extension).
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled

# Every positive target below must print #Top and exit 0. The modules partition
# the bounded domain to keep each prover invocation below the 8 GB memory cap.
kprove spec.k --definition verification-kompiled --spec-module SPEC-NEGATIVE
kprove spec.k --definition verification-kompiled --spec-module SPEC-02-11
kprove spec.k --definition verification-kompiled --spec-module SPEC-12-21
kprove spec.k --definition verification-kompiled --spec-module SPEC-22-31
kprove spec.k --definition verification-kompiled --spec-module SPEC-32-41
kprove spec.k --definition verification-kompiled --spec-module SPEC-42-51
kprove spec.k --definition verification-kompiled --spec-module SPEC-52-61
kprove spec.k --definition verification-kompiled --spec-module SPEC-62-71
kprove spec.k --definition verification-kompiled --spec-module SPEC-72-81
kprove spec.k --definition verification-kompiled --spec-module SPEC-82-91
kprove spec.k --definition verification-kompiled --spec-module SPEC-92-99
