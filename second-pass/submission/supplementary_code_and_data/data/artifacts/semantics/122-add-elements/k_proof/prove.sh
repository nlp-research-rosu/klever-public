#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# The K concrete-test program begins with the exact submitted function.
diff -u solution.py <(sed -n '1,6p' concrete_tests.py)
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Concrete execution under the required LLVM definition.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Symbolic definition and all proof claims.
kompile verification.k \
  --backend haskell \
  --main-module ADD-ELEMENTS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module ADD-ELEMENTS-SPEC
