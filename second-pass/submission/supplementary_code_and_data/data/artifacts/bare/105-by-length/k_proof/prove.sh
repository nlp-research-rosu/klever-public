#!/usr/bin/env bash
set -euo pipefail

# Recreate the submitted constructor term from the fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# Check the original Python examples before entering the K semantics.
python3 - <<'PY'
from solution import by_length

assert by_length([2, 1, 1, 4, 5, 8, 2, 3]) == [
    "Eight", "Five", "Four", "Three", "Two", "Two", "One", "One"
]
assert by_length([]) == []
assert by_length([1, -1, 55]) == ["One"]
print("Python examples: passed")
PY

# Compile the semantics and its verification vocabulary for symbolic execution.
definition_dir=.kbuild
rm -rf -- "$definition_dir"
kompile semantic.k \
  --backend haskell \
  --main-module MPY-COMPILED \
  --syntax-module MPY-SYNTAX \
  -o "$definition_dir"

# Exercise the translated program on every example from prompt.py.
krun solution.mpy -d "$definition_dir" \
  -cINPUT='pyList(2 :: 1 :: 1 :: 4 :: 5 :: 8 :: 2 :: 3 :: .PyVals)' \
  --output pretty
krun solution.mpy -d "$definition_dir" \
  -cINPUT='pyList(.PyVals)' \
  --output pretty
krun solution.mpy -d "$definition_dir" \
  -cINPUT='pyList(1 :: -1 :: 55 :: .PyVals)' \
  --output pretty

# Sanity check: a deliberately false postcondition must not prove.
if kprove mutation-spec.k -d "$definition_dir" \
    --spec-module BY-LENGTH-MUTATION-SPEC; then
  echo "ERROR: the deliberately false mutation unexpectedly proved" >&2
  exit 1
else
  echo "Mutation probe: rejected as expected"
fi

# Required positive target proof.  Success prints #Top and exits zero.
kprove spec.k -d "$definition_dir" --spec-module BY-LENGTH-SPEC
