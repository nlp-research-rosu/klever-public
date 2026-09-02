#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Regenerate the submitted constructor term and compile the semantics.
python3 py2mpy.py solution.py > solution.mpy
kompile semantic.k --backend haskell \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX

# Check that the concrete AST named in the proof is exactly solution.mpy.
cmp \
  <(kast solution.mpy -d semantic-kompiled -m MPY-SYNTAX \
      --output kore --expand-macros) \
  <(kast -d semantic-kompiled -m VERIFICATION -e 'solutionProgram' \
      --output kore --expand-macros)

# Exercise both examples from prompt.py through the K interpreter.
krun solution.mpy -d semantic-kompiled \
  -cLST1='Cons(1, Cons(2, Cons(3, Cons(4, Nil))))' \
  -cLST2='Cons(1, Cons(2, Cons(3, Cons(4, Nil))))' \
  --pattern '<result> "YES" </result>'
krun solution.mpy -d semantic-kompiled \
  -cLST1='Cons(1, Cons(2, Cons(3, Cons(4, Nil))))' \
  -cLST2='Cons(1, Cons(5, Cons(3, Cons(4, Nil))))' \
  --pattern '<result> "NO" </result>'

# Prove the loop invariant and both exhaustive result claims.
kprove spec.k -d semantic-kompiled --spec-module SPEC \
  --output pretty --smt-timeout 5000
