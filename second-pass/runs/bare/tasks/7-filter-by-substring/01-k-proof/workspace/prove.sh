#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

cd "$(dirname "$0")"

# Regenerate the constructor program from the immutable translator.
python3 py2mpy.py solution.py > solution.mpy

# Check the Python implementation, including duplicates and the empty substring.
python3 - <<'PY'
from solution import filter_by_substring

assert filter_by_substring([], "a") == []
assert filter_by_substring(
    ["abc", "bacd", "cde", "array"], "a"
) == ["abc", "bacd", "array"]
assert filter_by_substring(["x", "x", ""], "") == ["x", "x", ""]
PY

# Compile from a clean, explicitly scoped definition directory.
if [[ -d .kbuild/verification-kompiled ]]; then
  rm -rf -- .kbuild/verification-kompiled
fi
mkdir -p .kbuild
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  -o .kbuild/verification-kompiled

# Exercise the generated program with the two examples from prompt.py.
EMPTY_OUTPUT=$(krun solution.mpy \
  --definition .kbuild/verification-kompiled \
  -cFUNCTION='"filter_by_substring"' \
  -cINPUT='Nil' \
  -cSUBSTRING='"a"')
printf '%s\n' "$EMPTY_OUTPUT"
[[ "$EMPTY_OUTPUT" == $'<k>\n  Nil ~> .K\n</k>' ]]

PROMPT_OUTPUT=$(krun solution.mpy \
  --definition .kbuild/verification-kompiled \
  -cFUNCTION='"filter_by_substring"' \
  -cINPUT='Cons("abc",Cons("bacd",Cons("cde",Cons("array",Nil))))' \
  -cSUBSTRING='"a"')
printf '%s\n' "$PROMPT_OUTPUT"
[[ "$PROMPT_OUTPUT" == $'<k>\n  Cons ( "abc" , Cons ( "bacd" , Cons ( "array" , Nil ) ) ) ~> .K\n</k>' ]]

# Universal proof by structural induction: exact-program reduction, base case,
# and the exhaustive keep/drop constructor cases under the tail hypothesis.
kprove spec.k \
  --definition .kbuild/verification-kompiled \
  --spec-module SPEC \
  --claims UNIVERSAL-PROGRAM-REDUCTION
kprove spec.k \
  --definition .kbuild/verification-kompiled \
  --spec-module SPEC \
  --claims UNIVERSAL-BASE
kprove spec.k \
  --definition .kbuild/verification-kompiled \
  --spec-module SPEC \
  --claims UNIVERSAL-STEP-KEEP
kprove spec.k \
  --definition .kbuild/verification-kompiled \
  --spec-module SPEC \
  --claims UNIVERSAL-STEP-DROP

# Full-program prompt claims.
kprove spec.k \
  --definition .kbuild/verification-kompiled \
  --spec-module SPEC \
  --claims EMPTY-EXAMPLE
kprove spec.k \
  --definition .kbuild/verification-kompiled \
  --spec-module SPEC \
  --claims PROMPT-EXAMPLE
