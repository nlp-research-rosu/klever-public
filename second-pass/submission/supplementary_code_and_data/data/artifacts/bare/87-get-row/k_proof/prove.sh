#!/usr/bin/env bash
set -euo pipefail

# Recreate the translated program and check the ordinary Python examples.
python3 py2mpy.py solution.py > solution.mpy
python3 - <<'PY'
from solution import get_row

assert get_row([
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 1, 6],
    [1, 2, 3, 4, 5, 1],
], 1) == [(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)]
assert get_row([], 1) == []
assert get_row([[], [1], [1, 2, 3]], 3) == [(2, 2)]
PY

# Compile the executable semantics and exercise the translated solution.
kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --backend llvm
krun solution.mpy \
  --definition semantic-kompiled \
  -cLST='pyList(vcons(pyList(vcons(pyInt(1),vcons(pyInt(2),vcons(pyInt(1),vnil)))),vcons(pyList(vcons(pyInt(1),vnil)),vnil)))' \
  -cX='pyInt(1)' --output pretty
krun solution.mpy --definition semantic-kompiled \
  -cLST='pyList(vnil)' -cX='pyInt(1)' --output pretty

# Compile the proof definition and prove every claim in spec.k.
kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell
translated_term="$(mktemp)"
proved_term="$(mktemp)"
kast solution.mpy --definition verification-kompiled \
  --module MPY-SYNTAX --sort Program --output kore > "$translated_term"
kast --expression solutionProgram --definition verification-kompiled \
  --module VERIFICATION --sort Program --expand-macros --output kore > "$proved_term"
cmp "$translated_term" "$proved_term"
kprove spec.k --definition verification-kompiled --spec-module SPEC
