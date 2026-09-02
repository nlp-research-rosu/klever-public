#!/usr/bin/env bash
set -euo pipefail

# Regenerate the submitted constructor term with the required fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# Compile the semantics together with the verification-only oracle and program
# macro.  The Haskell backend is used by both krun and kprove below.
kompile verification.k \
  --backend haskell \
  --main-module ROMAN-VERIFICATION \
  --syntax-module MINI-PYTHON-SYNTAX

# Prove that the ground program macro in verification.k is exactly the AST
# generated from solution.py (after macro expansion).
diff -u \
  <(kast solution.mpy \
      --definition verification-kompiled \
      --module ROMAN-VERIFICATION \
      --sort Pgm \
      --output kast) \
  <(kast \
      --expression romanProgram \
      --definition verification-kompiled \
      --module ROMAN-VERIFICATION \
      --sort Pgm \
      --expand-macros \
      --output kast)

# Exercise both contract boundaries and all three examples from prompt.py.
krun solution.mpy --definition verification-kompiled -cINPUT=1 \
  | grep -F 'result ( vStr ( "i" ) )'
krun solution.mpy --definition verification-kompiled -cINPUT=19 \
  | grep -F 'result ( vStr ( "xix" ) )'
krun solution.mpy --definition verification-kompiled -cINPUT=152 \
  | grep -F 'result ( vStr ( "clii" ) )'
krun solution.mpy --definition verification-kompiled -cINPUT=426 \
  | grep -F 'result ( vStr ( "cdxxvi" ) )'
krun solution.mpy --definition verification-kompiled -cINPUT=1000 \
  | grep -F 'result ( vStr ( "m" ) )'

# Prove every claim in spec.k.  The sole claim is symbolic over 1 <= N <= 1000.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module ROMAN-SPEC
