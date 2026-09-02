#!/usr/bin/env bash
set -euo pipefail

# Recreate the constructor program from the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Compile the semantics and exercise the translated program on every prompt
# example. TEST is parsed at K sort String, hence the embedded double quotes.
kompile semantic.k --backend haskell \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  -Wno unused-symbol -Wno unused-var
krun solution.mpy --definition semantic-kompiled -cTEST='"a b c"' --output pretty
krun solution.mpy --definition semantic-kompiled -cTEST='"a b b a"' --output pretty
krun solution.mpy --definition semantic-kompiled -cTEST='"a b c a b"' --output pretty
krun solution.mpy --definition semantic-kompiled -cTEST='"b b b b a"' --output pretty
krun solution.mpy --definition semantic-kompiled -cTEST='""' --output pretty

# Prove the base and exhaustive one-iteration obligations without importing
# the induction-closure equations.
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  -Wno unused-symbol -Wno unused-var
kprove spec.k --definition verification-kompiled \
  --spec-module COUNT-LOOP-SPEC --output pretty \
  -Wno unused-symbol -Wno unused-var
kprove spec.k --definition verification-kompiled \
  --spec-module SELECT-LOOP-SPEC --output pretty \
  -Wno unused-symbol -Wno unused-var
kprove spec.k --definition verification-kompiled \
  --spec-module EXAMPLES-SPEC --output pretty \
  -Wno unused-symbol -Wno unused-var

# Compile the now-verified loop equations as reusable induction lemmas and
# prove the entry point equal to the denotational histogram for every token list
# and every space-separated input string.
kompile lemmas.k --backend haskell \
  --main-module VERIFIED-LOOP-LEMMAS --syntax-module MPY-SYNTAX \
  -Wno unused-symbol -Wno unused-var
kprove spec.k --definition lemmas-kompiled \
  --spec-module MAIN-CORRECTNESS-SPEC --output pretty \
  -Wno unused-symbol -Wno unused-var
