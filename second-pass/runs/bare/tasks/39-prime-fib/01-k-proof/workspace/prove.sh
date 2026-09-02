#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor program using the supplied, unmodified translator.
python3 py2mpy.py solution.py > solution.mpy

# Check the Python implementation independently on the prompt examples and
# several later sequence elements.
python3 - <<'PY'
from solution import prime_fib

expected = [2, 3, 5, 13, 89, 233, 1597, 28657, 514229, 433494437]
actual = [prime_fib(n) for n in range(1, len(expected) + 1)]
assert actual == expected, (actual, expected)
PY

# Compile and exercise the ordinary small-step semantics.
kompile --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm -o semantic-kompiled semantic.k
for n in 1 2 3 4 5; do
  krun solution.mpy -d semantic-kompiled -cN="$n" --output pretty
done

# Prove full concrete interpreter executions without verification summaries.
kompile --main-module PRIME-FIB-PROGRAM \
  --syntax-module PRIME-FIB-PROGRAM \
  --backend haskell -o concrete-kompiled verification.k
kprove concrete-spec.k -d concrete-kompiled \
  --spec-module CONCRETE-SPEC --color off

# Prove the general positive-input claim and every example claim in spec.k.
kompile --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --backend haskell -o verification-kompiled verification.k
kprove spec.k -d verification-kompiled --spec-module SPEC --color off
