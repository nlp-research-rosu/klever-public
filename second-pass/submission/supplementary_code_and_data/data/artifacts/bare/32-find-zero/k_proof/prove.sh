#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor tree from the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Compile the standalone semantics, then the semantics plus proof utilities.
kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION

# Exercise the actual freshly generated solution.mpy term with the prompt's
# linear example.  The exact rational result is approximately -0.5.
TRANSLATED_PROGRAM="$(< solution.mpy)"
krun --definition verification-kompiled \
  -cPGM="$TRANSLATED_PROGRAM ;; Invoke(\"find_zero\", list(ListItem(rat(1, 1)) ListItem(rat(2, 1))))" \
  --output pretty

# Exercise the second prompt example and independently check its residual.
krun --definition verification-kompiled \
  -cPGM="$TRANSLATED_PROGRAM ;; VerifyRoot(ListItem(rat(-6, 1)) ListItem(rat(11, 1)) ListItem(rat(-6, 1)) ListItem(rat(1, 1)), Invoke(\"find_zero\", list(ListItem(rat(-6, 1)) ListItem(rat(11, 1)) ListItem(rat(-6, 1)) ListItem(rat(1, 1)))), rat(1, 100000000))" \
  --output pretty

# This is the required positive target-proof command.  It proves every claim
# in spec.k and must print #Top and exit zero.
kprove spec.k \
  --definition verification-kompiled \
  --output pretty
