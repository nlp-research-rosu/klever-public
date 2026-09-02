#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy
kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX

krun solution.mpy -cINPUT='""' --definition semantic-kompiled
krun solution.mpy -cINPUT='"hi"' --definition semantic-kompiled
krun solution.mpy -cINPUT='"asdfghjkl"' --definition semantic-kompiled
krun solution.mpy -cINPUT='"gf"' --definition semantic-kompiled
krun solution.mpy -cINPUT='"et"' --definition semantic-kompiled
krun solution.mpy -cINPUT='"xyz"' --definition semantic-kompiled

kprove spec.k --definition semantic-kompiled --spec-module SPEC
