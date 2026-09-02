#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Regenerate the constructor program from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Pin the program parsed by krun to the exact constructor tree named
# solutionPgm in verification.k.  A source/translation mutation must therefore
# update (and re-prove) the specification rather than silently proving a stale
# copy of the program.
test "$(sha256sum solution.mpy | cut -d' ' -f1)" = \
  "f000e03ceb98957592a0d397f7e51aad729823b556ab7fdfb749b5fb8defc28e"

# Concrete execution uses the fast LLVM backend.
kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-llvm-kompiled

krun solution.mpy --definition semantic-llvm-kompiled \
  -cS='"abcde"' -cC='"ae"'
krun solution.mpy --definition semantic-llvm-kompiled \
  -cS='"abcdef"' -cC='"b"'
krun solution.mpy --definition semantic-llvm-kompiled \
  -cS='"abcdedcba"' -cC='"ab"'

# Symbolic proof uses the Haskell/Kore backend.  This single kprove command
# proves every claim in spec.k: the arbitrary-input theorem and all examples.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled
