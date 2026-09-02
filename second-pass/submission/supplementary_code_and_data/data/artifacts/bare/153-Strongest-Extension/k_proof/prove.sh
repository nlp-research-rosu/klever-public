#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Regenerate the required transliteration from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Compile the semantics together with the verification-only contract oracle.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  -o verification-kompiled

# Prove that the readable StrongestProgram macro in verification.k is exactly
# the constructor tree generated in solution.mpy.
cmp \
  <(kast solution.mpy --definition verification-kompiled --sort Program --output kore) \
  <(kast verification-input.mpy --definition verification-kompiled --sort Program --output kore)

# Exercise the actual translated program.  Limit display to the result cell.
krun solution.mpy --definition verification-kompiled \
  -cCLASS='"Slices"' \
  -cEXTENSIONS='strVal("SErviNGSliCes");strVal("Cheese");strVal("StuFfed")' \
  | sed -n '/<result>/,/<\/result>/p'

krun solution.mpy --definition verification-kompiled \
  -cCLASS='"my_class"' \
  -cEXTENSIONS='strVal("AA");strVal("Be");strVal("CC")' \
  | sed -n '/<result>/,/<\/result>/p'

# Positive target proof: this proves every claim in spec.k.
kprove spec.k --definition verification-kompiled --spec-module SPEC
