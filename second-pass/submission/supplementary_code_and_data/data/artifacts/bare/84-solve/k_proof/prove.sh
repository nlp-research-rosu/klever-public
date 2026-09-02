#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy

python3 - <<'PY'
from solution import solve

for n in range(10001):
    expected = format(sum(int(digit) for digit in str(n)), "b")
    assert solve(n) == expected, (n, solve(n), expected)
print("CPython exhaustive check: 10001 inputs passed")
PY

kompile \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  -o semantic-kompiled-haskell \
  semantic.k

# Check that the program constant used by the proof is exactly the parsed
# solution.mpy term after macro expansion.
TERM_CHECK_DIR=$(mktemp -d)
trap 'rm -rf "$TERM_CHECK_DIR"' EXIT
kast solution.mpy \
  --definition semantic-kompiled-haskell \
  --module MPY-SYNTAX \
  --sort Pgm \
  --output json \
  --output-file "$TERM_CHECK_DIR/translated.json"
kast \
  --expression solutionProgram \
  --definition semantic-kompiled-haskell \
  --module VERIFICATION \
  --sort Pgm \
  --expand-macros \
  --output json \
  --output-file "$TERM_CHECK_DIR/embedded.json"
cmp "$TERM_CHECK_DIR/translated.json" "$TERM_CHECK_DIR/embedded.json"

krun solution.mpy --definition semantic-kompiled-haskell -cN=0
krun solution.mpy --definition semantic-kompiled-haskell -cN=1000
krun solution.mpy --definition semantic-kompiled-haskell -cN=150
krun solution.mpy --definition semantic-kompiled-haskell -cN=147
krun solution.mpy --definition semantic-kompiled-haskell -cN=10000

# The eleven commands run by xargs prove every named claim in spec.k.  Four
# independent prover processes keep total memory comfortably below 8 GB.
printf '%s\n' \
  SPEC.inputs-00000-00999 \
  SPEC.inputs-01000-01999 \
  SPEC.inputs-02000-02999 \
  SPEC.inputs-03000-03999 \
  SPEC.inputs-04000-04999 \
  SPEC.inputs-05000-05999 \
  SPEC.inputs-06000-06999 \
  SPEC.inputs-07000-07999 \
  SPEC.inputs-08000-08999 \
  SPEC.inputs-09000-09999 \
  SPEC.input-10000 \
  | xargs -n1 -P4 sh -c \
      'kprove spec.k --definition semantic-kompiled-haskell --spec-module SPEC --claims "$1"' _
