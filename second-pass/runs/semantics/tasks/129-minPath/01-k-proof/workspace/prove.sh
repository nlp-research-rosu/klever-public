#!/usr/bin/env bash
set -euo pipefail

# Regenerate the submitted constructor term from the submitted Python.
python3 py2mpy.py solution.py > solution.mpy

# The concrete driver contains the exact submitted function followed by tests.
head -n 38 concrete-tests.py | cmp - solution.py
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Concrete execution under the supplied LLVM semantics.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# Symbolic execution and proof under MPY (without the concrete-only module).
kompile verification.k \
  --backend haskell \
  --main-module MINPATH-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module MINPATH-SPEC
