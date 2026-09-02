#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Translate the submitted implementation and bind it to the constructor term
# represented by solutionProgram/belowZeroFunctionBody in verification.k.
python3 py2mpy.py solution.py > solution.mpy
test "$(sha256sum solution.mpy | cut -d ' ' -f 1)" = \
  "5e9e907167be11a2f30b29f110fb940b866c050c1efacbb6f638a39bfc96bab5"

# Concrete execution with the required LLVM main and syntax modules.
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# First prove the universal loop invariant using only MPY plus the typed-list
# proof representation. This makes no loop-summary rule available.
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module AUX-SPEC

# Then import that exact proved invariant as a high-priority summary and prove
# the complete translated module, including definition load and function call.
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-lemma-kompiled
kprove spec.k \
  --definition verification-lemma-kompiled \
  --spec-module MAIN-SPEC
