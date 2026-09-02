#!/usr/bin/env bash
set -euo pipefail

# Recreate the translated program from the unmodified fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# Ensure the exact term proved below is parser-normalized equivalent to the
# current translator output (the markers delimit its macro RHS).
python3 - <<'PY'
from pathlib import Path

verification = Path("verification.k").read_text()
marked = verification.split("// BEGIN EXACT SOLUTION TERM", 1)[1]
marked = marked.split("// END EXACT SOLUTION TERM", 1)[0]
embedded = marked.split("rule solutionProgram =>", 1)[1]
translated = Path("solution.mpy").read_text()
embedded = "".join(embedded.split()).replace(".Stmts", "")
translated = "".join(translated.split())
assert embedded == translated
print("Embedded proof term matches solution.mpy: ok")
PY

# Check the Python implementation, including unequal lengths (zip behavior).
python3 - <<'PY'
from solution import string_xor

assert string_xor("010", "110") == "100"
assert string_xor("0101", "11") == "10"
assert string_xor("", "101") == ""
assert string_xor("101", "") == ""

for na in range(6):
    for nb in range(6):
        for x in range(1 << na):
            for y in range(1 << nb):
                a = format(x, f"0{na}b") if na else ""
                b = format(y, f"0{nb}b") if nb else ""
                expected = "".join(str(int(p) ^ int(q)) for p, q in zip(a, b))
                assert string_xor(a, b) == expected
print("Python exhaustive check for lengths 0..5: ok")
PY

# Compile and exercise the concrete semantics on the prompt example.
kompile semantic.k \
  --main-module XOR \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition final-semantic-kompiled

krun solution.mpy \
  --definition final-semantic-kompiled \
  -cARGS='Args(str(cons(false,cons(true,cons(false,empty)))),str(cons(true,cons(true,cons(false,empty)))))' \
  --output pretty

# Compile the symbolic verification layer and prove every claim in spec.k.
kompile verification.k \
  --main-module XOR-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition final-verification-kompiled

kprove spec.k \
  --spec-module XOR-SPEC \
  --definition final-verification-kompiled \
  --output pretty
