#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX

krun solution.mpy --definition semantic-kompiled -cINPUT='""'
krun solution.mpy --definition semantic-kompiled -cINPUT='"Hi"'
krun solution.mpy --definition semantic-kompiled -cINPUT='"hello"'
krun solution.mpy --definition semantic-kompiled -cINPUT='"Hello World!!!"'
krun solution.mpy --definition semantic-kompiled -cINPUT='"  ba  dc "'

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Prove the insertion lemma without assumptions.
kprove spec.k \
  --definition verification-kompiled \
  --claims SPEC.insert-correct

# The scanner proof consumes the independently proved insertion lemma.
kprove spec.k \
  --definition verification-kompiled \
  --claims SPEC.insert-correct,SPEC.process-correct \
  --trusted SPEC.insert-correct

# Prove every remaining claim, including the universal theorem and examples,
# using the two lemmas established by the preceding commands.
kprove spec.k \
  --definition verification-kompiled \
  --trusted SPEC.insert-correct,SPEC.process-correct
