#!/usr/bin/env bash
set -euo pipefail

# Recreate the translated constructor program from the submitted Python.
python3 py2mpy.py solution.py > solution.mpy

# Build the executable semantics and exercise all prompt examples.
kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX
krun solution.mpy --definition semantic-kompiled \
  -cINPUT='VList(cons(4, cons(1, cons(2, cons(2, cons(3, cons(1, .Ints)))))))'
krun solution.mpy --definition semantic-kompiled \
  -cINPUT='VList(cons(1, cons(2, cons(2, cons(3, cons(3, cons(3, cons(4, cons(4, cons(4, .Ints))))))))))'
krun solution.mpy --definition semantic-kompiled \
  -cINPUT='VList(cons(5, cons(5, cons(4, cons(4, cons(4, .Ints))))))'

# First prove the generalized loop summary using only the raw small-step rules.
kompile verification-core.k --backend haskell \
  --main-module VERIFICATION-CORE --syntax-module MPY-SYNTAX
kprove loop-lemma-spec.k --definition verification-core-kompiled \
  --spec-module LOOP-LEMMA-SPEC

# Compile that proved summary as a derived verification rule, then prove every
# concrete and universal end-to-end claim in spec.k.
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled --spec-module SPEC
