#!/usr/bin/env bash
set -euo pipefail

# Regenerate the submitted constructor tree from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Check the original prompt examples in CPython as a front-end sanity check.
python3 - <<'PY'
from solution import total_match

examples = [
    (([], []), []),
    ((['hi', 'admin'], ['hI', 'Hi']), ['hI', 'Hi']),
    ((['hi', 'admin'], ['hi', 'hi', 'admin', 'project']), ['hi', 'admin']),
    ((['hi', 'admin'], ['hI', 'hi', 'hi']), ['hI', 'hi', 'hi']),
    ((['4'], ['1', '2', '3', '4', '5']), ['4']),
]

for arguments, expected in examples:
    assert total_match(*arguments) == expected
print('CPython prompt examples: passed')
PY

# Compile the semantics together with the verifier functions used by spec.k.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Exercise every prompt example through the K semantics.
krun solution.mpy -d verification-kompiled \
  -cARGS='args(pyList(.StrVals),pyList(.StrVals))'
krun solution.mpy -d verification-kompiled \
  -cARGS='args(pyList(pyStr("hi") :: pyStr("admin") :: .StrVals),pyList(pyStr("hI") :: pyStr("Hi") :: .StrVals))'
krun solution.mpy -d verification-kompiled \
  -cARGS='args(pyList(pyStr("hi") :: pyStr("admin") :: .StrVals),pyList(pyStr("hi") :: pyStr("hi") :: pyStr("admin") :: pyStr("project") :: .StrVals))'
krun solution.mpy -d verification-kompiled \
  -cARGS='args(pyList(pyStr("hi") :: pyStr("admin") :: .StrVals),pyList(pyStr("hI") :: pyStr("hi") :: pyStr("hi") :: .StrVals))'
krun solution.mpy -d verification-kompiled \
  -cARGS='args(pyList(pyStr("4") :: .StrVals),pyList(pyStr("1") :: pyStr("2") :: pyStr("3") :: pyStr("4") :: pyStr("5") :: .StrVals))'

# Prove every claim in spec.k.  Success prints #Top and exits zero.
kprove spec.k -d verification-kompiled
