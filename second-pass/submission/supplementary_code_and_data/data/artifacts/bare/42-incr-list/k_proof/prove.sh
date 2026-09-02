#!/usr/bin/env bash
set -euo pipefail

# Recreate the constructor program from the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Check the Python implementation against the prompt examples and edge cases.
python3 - <<'PY'
from solution import incr_list

assert incr_list([1, 2, 3]) == [2, 3, 4]
assert incr_list([5, 3, 5, 2, 3, 3, 9, 0, 123]) == [6, 4, 6, 3, 4, 4, 10, 1, 124]
assert incr_list([]) == []
original = [1, -2]
answer = incr_list(original)
assert answer == [2, -1]
assert original == [1, -2]
assert answer is not original
PY

# Compile the semantics used for both execution and proof.
kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX

# Exercise the translated program in K. A successful closed pattern is #Top.
krun -d semantic-kompiled \
  -cARGS='pyList(ListItem(pyInt(1)) ListItem(pyInt(2)) ListItem(pyInt(3)))' \
  --pattern '<result> result(pyList(ListItem(pyInt(2)) ListItem(pyInt(3)) ListItem(pyInt(4)))) </result>' \
  solution.mpy

krun -d semantic-kompiled \
  -cARGS='pyList(ListItem(pyInt(5)) ListItem(pyInt(3)) ListItem(pyInt(5)) ListItem(pyInt(2)) ListItem(pyInt(3)) ListItem(pyInt(3)) ListItem(pyInt(9)) ListItem(pyInt(0)) ListItem(pyInt(123)))' \
  --pattern '<result> result(pyList(ListItem(pyInt(6)) ListItem(pyInt(4)) ListItem(pyInt(6)) ListItem(pyInt(3)) ListItem(pyInt(4)) ListItem(pyInt(4)) ListItem(pyInt(10)) ListItem(pyInt(1)) ListItem(pyInt(124)))) </result>' \
  solution.mpy

krun -d semantic-kompiled \
  -cARGS='pyList(.List)' \
  --pattern '<result> result(pyList(.List)) </result>' \
  solution.mpy

# Prove every claim in SPEC (the invariant and whole-program theorem).
kprove spec.k --definition semantic-kompiled
