#!/usr/bin/env bash
set -euo pipefail

# Recreate the submitted constructor program from the immutable translator.
python3 py2mpy.py solution.py > solution.mpy

# Compile and exercise the actual generated program under our semantics.
kompile semantic.k \
  --backend haskell \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX

krun solution.mpy \
  --definition semantic-kompiled \
  -cSENTENCE='"This is a test"' \
  | grep -F 'Str ( "is" )'

krun solution.mpy \
  --definition semantic-kompiled \
  -cSENTENCE='"lets go for swimming"' \
  | grep -F 'Str ( "go for" )'

# Compile the proof/oracle extension.
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX

# 1. Prove the induction lemma for every WordSeq and accumulator.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module WORDS-IN-SENTENCE-SPEC \
  --claims WORDS-IN-SENTENCE-SPEC.loop-invariant \
  --output pretty

# 2. Use only that now-proved lemma to close the raw-string symbolic contract.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module WORDS-IN-SENTENCE-SPEC \
  --claims WORDS-IN-SENTENCE-SPEC.loop-invariant,WORDS-IN-SENTENCE-SPEC.symbolic-contract \
  --trusted WORDS-IN-SENTENCE-SPEC.loop-invariant \
  --output pretty

# 3. Prove all concrete witnesses, including both prompt examples and bounds.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module WORDS-IN-SENTENCE-SPEC \
  --claims WORDS-IN-SENTENCE-SPEC.example-one,WORDS-IN-SENTENCE-SPEC.example-two,WORDS-IN-SENTENCE-SPEC.length-boundaries,WORDS-IN-SENTENCE-SPEC.composite-hundred \
  --output pretty
