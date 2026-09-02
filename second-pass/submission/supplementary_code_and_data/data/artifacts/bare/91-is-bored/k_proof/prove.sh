#!/bin/sh
set -eu

# Recreate the constructor term with the mandated fixed translator.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

# Compile and exercise the actual solution.mpy term on both prompt examples.
kompile semantic.k --backend haskell --syntax-module MPY-SYNTAX --main-module MPY
krun solution.mpy --definition semantic-kompiled -cINPUT='"Hello world"'
krun solution.mpy --definition semantic-kompiled -cINPUT='"The sky is blue. The sun is shining. I love this weather"'

# Compile the contract model and prove every reachability claim in spec.k.
kompile verification.k --backend haskell --syntax-module MPY-SYNTAX --main-module VERIFICATION
kprove spec.k --definition verification-kompiled --spec-module SPEC
