#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the constructor program using the supplied, unmodified translator.
python3 py2mpy.py solution.py > solution.mpy

# Compile the executable semantics and exercise every example from prompt.py.
kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-llvm-kompiled

krun solution.mpy -d semantic-llvm-kompiled -cINPUT='""' --output pretty \
  | grep -F 'intVal ( 0 )'
krun solution.mpy -d semantic-llvm-kompiled -cINPUT='"abAB"' --output pretty \
  | grep -F 'intVal ( 131 )'
krun solution.mpy -d semantic-llvm-kompiled -cINPUT='"abcCd"' --output pretty \
  | grep -F 'intVal ( 67 )'
krun solution.mpy -d semantic-llvm-kompiled -cINPUT='"helloE"' --output pretty \
  | grep -F 'intVal ( 69 )'
krun solution.mpy -d semantic-llvm-kompiled -cINPUT='"woArBld"' --output pretty \
  | grep -F 'intVal ( 131 )'
krun solution.mpy -d semantic-llvm-kompiled -cINPUT='"aAaaaXa"' --output pretty \
  | grep -F 'intVal ( 153 )'

# Build the symbolic definition and prove every claim in spec.k.
kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-haskell-kompiled

kprove \
  --definition semantic-haskell-kompiled \
  --spec-module SPEC \
  spec.k
