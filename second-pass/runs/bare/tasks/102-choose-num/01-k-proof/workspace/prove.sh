#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the submitted constructor term from the unmodified translator.
python3 py2mpy.py solution.py > solution.mpy

# A finite oracle check complements (but does not replace) the symbolic proof.
python3 - <<'PY'
from solution import choose_num

for x in range(1, 41):
    for y in range(1, 41):
        evens = [n for n in range(x, y + 1) if n % 2 == 0]
        expected = max(evens) if evens else -1
        assert choose_num(x, y) == expected, (x, y)
PY

# The verification module is included in the compiled definition because its
# chooseNumProgram term is the exact constructor tree emitted in solution.mpy.
kompile semantic.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Execute the translated program on the prompt example and the odd singleton
# boundary case. Fail if either final value is not the expected one.
example_output="$(krun run-12-15.mpy --definition semantic-kompiled)"
printf '%s\n' "$example_output"
grep -Fq 'VInt ( 14 )' <<<"$example_output"

boundary_output="$(krun run-13-13.mpy --definition semantic-kompiled)"
printf '%s\n' "$boundary_output"
grep -Fq 'VInt ( -1 )' <<<"$boundary_output"

# Prove all eight claims: four exact-result claims over an exhaustive input
# partition and four corresponding end-to-end contract claims.
kprove spec.k \
  --definition semantic-kompiled \
  --spec-module SPEC
