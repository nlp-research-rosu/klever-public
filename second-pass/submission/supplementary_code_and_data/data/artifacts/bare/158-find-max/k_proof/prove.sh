#!/usr/bin/env bash
set -eu

# Recreate the required constructor term from the unmodified translator.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

# One Haskell definition supports both concrete execution and symbolic proof.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  -I .

# All three examples from prompt.py, executed from the generated solution.mpy.
krun solution.mpy --definition verification-kompiled \
  -cINPUT='cons("name", cons("of", cons("string", nil)))' \
  --pattern '<result> result(strVal("string")) </result>' \
  --output pretty

krun solution.mpy --definition verification-kompiled \
  -cINPUT='cons("name", cons("enam", cons("game", nil)))' \
  --pattern '<result> result(strVal("enam")) </result>' \
  --output pretty

krun solution.mpy --definition verification-kompiled \
  -cINPUT='cons("aaaaaaa", cons("bb", cons("cc", nil)))' \
  --pattern '<result> result(strVal("aaaaaaa")) </result>' \
  --output pretty

# Prove every claim: exact-program initialization, the universal loop
# invariant, and their direct end-to-end composition.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
