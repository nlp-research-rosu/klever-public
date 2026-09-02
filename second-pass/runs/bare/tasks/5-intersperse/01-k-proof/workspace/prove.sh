#!/usr/bin/env bash
set -euo pipefail
set -x

# The committed constructor term must be exactly the fixed translator's output.
python3 py2mpy.py solution.py | cmp - solution.mpy

# Concrete execution backend and both contract boundary/example runs.
kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX
krun run-empty.mpy --definition semantic-kompiled \
  | grep -F 'VList ( [ .Ints ] )'
krun run-example.mpy --definition semantic-kompiled \
  | grep -F 'VList ( [ 1 , 4 , 2 , 4 , 3 , .Ints ] )'

# Symbolic backend and the universally quantified reachability proof.
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled
