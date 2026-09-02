#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy

# verification.k names this exact constructor tree #solution.  Pinning the
# regenerated tree prevents the proof from drifting away from solution.py.
printf '%s  %s\n' \
  'fd871e9b9fe673932b6f77f16595ee6a0fea1ae8d74e89c8fca2e0b11a1e604c' \
  'solution.mpy' | sha256sum --check -

python3 - <<'PY'
from itertools import product
from solution import is_happy

def oracle(s):
    return len(s) >= 3 and all(
        len(set(s[i:i + 3])) == 3 for i in range(len(s) - 2)
    )

for size in range(8):
    for letters in product("abc", repeat=size):
        text = "".join(letters)
        assert is_happy(text) == oracle(text)
PY

kompile semantic.k \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition semantic-kompiled

krun solution.mpy -cINPUT='eps' --definition semantic-kompiled
krun solution.mpy -cINPUT='ch(97, eps)' --definition semantic-kompiled
krun solution.mpy -cINPUT='ch(97, ch(97, eps))' --definition semantic-kompiled
krun solution.mpy -cINPUT='ch(97, ch(98, ch(99, ch(100, eps))))' --definition semantic-kompiled
krun solution.mpy -cINPUT='ch(97, ch(97, ch(98, ch(98, eps))))' --definition semantic-kompiled
krun solution.mpy -cINPUT='ch(97, ch(100, ch(98, eps)))' --definition semantic-kompiled
krun solution.mpy -cINPUT='ch(120, ch(121, ch(121, eps)))' --definition semantic-kompiled

kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled
