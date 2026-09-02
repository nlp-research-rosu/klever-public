#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Translate the submitted implementation and the concrete assertion harness.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Required concrete LLVM definition and execution.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled --output none

# Prove the inductive loop invariant against MPY without its summary rule.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC

# Compose that proved invariant with call/setup/return semantics and prove the
# public contract (symbolic n < 0, the n = 0 boundary, and symbolic n >= 1).
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module FULL-SPEC
