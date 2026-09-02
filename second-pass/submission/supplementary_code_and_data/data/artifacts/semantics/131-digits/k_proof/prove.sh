#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# The concrete harness repeats exactly the submitted function, then adds
# assertions.  Fail early if the repeated function ever diverges.
diff -u solution.py <(sed -n '1,10p' concrete-tests.py)
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Concrete execution uses the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled --output none
krun concrete-tests.mpy --definition runtime-kompiled --output none

# Symbolic execution imports MPY through verification.k, never MPY-KRUN.
kompile verification.k \
  --backend haskell \
  --main-module DIGITS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module DIGITS-SPEC |
  tee kprove.stdout

# Make the success criterion explicit in addition to kprove's exit status.
grep -qx '#Top' kprove.stdout
