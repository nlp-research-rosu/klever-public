#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the constructor program from the unmodified fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# Concrete execution uses the fast LLVM backend.
kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-PROGRAM-PARSING \
  --output-definition semantic-llvm-kompiled

krun solution.mpy \
  --definition semantic-llvm-kompiled \
  -cINPUT='"o o| .| o| o| .| .| .| .| o o"'
krun solution.mpy --definition semantic-llvm-kompiled -cINPUT='"o"'
krun solution.mpy --definition semantic-llvm-kompiled -cINPUT='"o|"'
krun solution.mpy --definition semantic-llvm-kompiled -cINPUT='".|"'

# Symbolic execution and reachability proofs use the Haskell backend.
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-PROGRAM-PARSING \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
