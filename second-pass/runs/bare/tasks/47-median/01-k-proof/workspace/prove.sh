#!/usr/bin/env bash
set -euo pipefail

# Recreate the pure AST-constructor translation and compile our semantics for
# both concrete execution (krun) and symbolic reachability proof (kprove).
python3 py2mpy.py solution.py > solution.mpy
kompile semantic.k \
  --main-module SEMANTIC \
  --syntax-module MEDIAN-SYNTAX \
  --backend haskell

# Exercise both examples from prompt.py through the K semantics.
krun solution.mpy \
  -cINPUT='cons(3, cons(1, cons(2, cons(4, cons(5, nil)))))'
krun solution.mpy \
  -cINPUT='cons(-10, cons(4, cons(6, cons(1000, cons(10, cons(20, nil))))))'

# Prove the universal refinement claim and both direct example claims.
kprove spec.k --definition semantic-kompiled --spec-module SPEC
