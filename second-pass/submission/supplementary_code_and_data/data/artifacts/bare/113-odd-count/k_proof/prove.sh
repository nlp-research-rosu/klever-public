#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the exact translator artifact and sanity-check the CPython program.
python3 py2mpy.py solution.py > solution.mpy
python3 - <<'PY'
from solution import odd_count

assert odd_count(["1234567"]) == [
    "the number of odd elements 4n the str4ng 4 of the 4nput."
]
assert odd_count(["3", "11111111"]) == [
    "the number of odd elements 1n the str1ng 1 of the 1nput.",
    "the number of odd elements 8n the str8ng 8 of the 8nput.",
]
PY

# Compile the executable semantics and run the translated first prompt example.
kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  -o semantic-kompiled

krun solution.mpy \
  -cINPUT='pyList(value(pyString(inputDigits(digit(oddDigit, digit(evenDigit, digit(oddDigit, digit(evenDigit, digit(oddDigit, digit(evenDigit, digit(oddDigit, noDigits))))))))), noValues))' \
  --definition semantic-kompiled \
  --output pretty

# Compile the proof definition.  The KAST comparison guarantees that the
# readable solutionProgram macro proved below is exactly solution.mpy.
kompile verification.k \
  --main-module ODD-COUNT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  -o verification-kompiled

cmp \
  <(kast solution.mpy \
      --definition verification-kompiled \
      --module MPY-SYNTAX \
      --sort Module \
      --expand-macros \
      --output kore) \
  <(kast \
      --expression solutionProgram \
      --definition verification-kompiled \
      --module ODD-COUNT-VERIFICATION \
      --sort Module \
      --expand-macros \
      --output kore)

# The deliberately false claim must be rejected; this guards against a
# vacuous proof harness.  Its expected non-zero result is handled explicitly.
if kprove mutation.k \
     --definition verification-kompiled \
     --spec-module ODD-COUNT-MUTATION \
     --output pretty; then
  echo "error: mutation.k unexpectedly proved" >&2
  exit 1
else
  echo "mutation.k rejected as expected"
fi

# Positive target proof: every claim in spec.k must close and print #Top.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module ODD-COUNT-SPEC \
  --output pretty
