#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recheck that the committed constructor term is exactly the translator output.
cmp solution.mpy <(python3 py2mpy.py solution.py)

# Check the Python implementation independently on examples and edge cases.
python3 - <<'PY'
from solution import count_upper

tests = {
    "aBCdEf": 1,
    "abcdefg": 0,
    "dBBE": 0,
    "": 0,
    "AEIOU": 3,
    "xA": 0,
}
for text, expected in tests.items():
    assert count_upper(text) == expected, (text, count_upper(text), expected)
PY

mkdir -p .build

# Compile the executable semantics and exercise the translated program.
kompile semantic.k \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  -o .build/semantic-kompiled

krun solution.mpy -cINPUT='"aBCdEf"' \
  --definition .build/semantic-kompiled | grep -F 'intVal ( 1 )'
krun solution.mpy -cINPUT='"abcdefg"' \
  --definition .build/semantic-kompiled | grep -F 'intVal ( 0 )'
krun solution.mpy -cINPUT='"dBBE"' \
  --definition .build/semantic-kompiled | grep -F 'intVal ( 0 )'

# Compile the verification extension and prove every claim in spec.k.
kompile verification.k \
  --main-module COUNT-UPPER-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  -o .build/verification-kompiled

kprove spec.k \
  --spec-module COUNT-UPPER-SPEC \
  --definition .build/verification-kompiled
