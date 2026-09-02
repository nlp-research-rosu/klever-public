#!/usr/bin/env bash
set -euo pipefail

# Regenerate the K constructor program from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Compile the executable semantics and exercise both branches (plus larger
# concrete instances) through the actual generated solution.mpy term.
kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled
krun solution.mpy --definition semantic-kompiled -cN=1
krun solution.mpy --definition semantic-kompiled -cN=2
krun solution.mpy --definition semantic-kompiled -cN=3
krun solution.mpy --definition semantic-kompiled -cN=5

# Compile the verification layer and prove every claim in spec.k.  This is the
# required positive target-proof command; success prints #Top and exits zero.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled
