#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output pretty

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled

kprove spec.k \
  --definition verification-base-kompiled \
  --claims SPEC.decode-loop \
  --output pretty

kprove spec.k \
  --definition verification-base-kompiled \
  --claims SPEC.char-inverse \
  --output pretty

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-WITH-LOOP \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --claims SPEC.decode-shift \
  --output pretty
