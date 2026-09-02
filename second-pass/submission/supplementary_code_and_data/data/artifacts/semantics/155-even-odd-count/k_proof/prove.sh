#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 -c 'from pathlib import Path; s = Path("solution.py").read_text(); t = Path("concrete_tests.py").read_text(); assert t.startswith(s)'
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module EVEN-ODD-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled

kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module EVEN-ODD-LOOP-SPEC

kompile verification.k \
  --backend haskell \
  --main-module EVEN-ODD-VERIFICATION-SUMMARY \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module EVEN-ODD-SPEC
