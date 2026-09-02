#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Translate the submitted Python and ensure it is the AST proved below.
python3 py2mpy.py solution.py > solution.mpy
printf '%s  %s\n' \
  '8b599b1860c8633b4dbb68bce7b2fcf8b276139506a85bcb7df42801e4969883' \
  solution.mpy | sha256sum -c -

# Concrete execution uses the LLVM backend.
kompile semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --warnings none
krun solution.mpy -d semantic-kompiled -cINPUT='"example.txt"' \
  | grep -F 'VStr ( "Yes" )'
krun solution.mpy -d semantic-kompiled -cINPUT='"1example.dll"' \
  | grep -F 'VStr ( "No" )'
krun solution.mpy -d semantic-kompiled -cINPUT='"a1b2c3.exe"' \
  | grep -F 'VStr ( "Yes" )'
krun solution.mpy -d semantic-kompiled -cINPUT='"a1b2c3d4.exe"' \
  | grep -F 'VStr ( "No" )'
krun solution.mpy -d semantic-kompiled -cINPUT='"a.b.txt"' \
  | grep -F 'VStr ( "No" )'
krun solution.mpy -d semantic-kompiled -cINPUT='"A.dll"' \
  | grep -F 'VStr ( "Yes" )'

# Universal symbolic proof uses the Haskell backend.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --warnings none
kprove spec.k --definition verification-kompiled --warnings none \
  | tee kprove.out
grep -qx '#Top' kprove.out

# Mutation sensitivity: this deliberately false claim must fail.
if kprove mutation-spec.k \
     --definition verification-kompiled \
     --warnings none > mutation-kprove.out 2>&1; then
  echo 'mutation probe unexpectedly proved' >&2
  exit 1
fi
