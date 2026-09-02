#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy

python3 - <<'PY'
import ast
import re
from pathlib import Path

solution = ast.parse(Path("solution.py").read_text()).body[0]
smoke = ast.parse(Path("concrete-smoke.py").read_text()).body[0]
assert ast.dump(solution, include_attributes=False) == ast.dump(
    smoke, include_attributes=False
)

def squash(text):
    return re.sub(r"\s+", "", text)

translated = squash(Path("solution.mpy").read_text())
formal_spec = squash(Path("spec.k").read_text())
assert translated in formal_spec

print("function_ast_equal: True")
print("translated_program_in_spec: True")
PY

python3 concrete-smoke.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
then
  echo "UNEXPECTED SUCCESS: false-postcondition mutation"
  exit 1
else
  echo "EXPECTED FAILURE: false-postcondition mutation"
fi

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
then
  echo "UNEXPECTED SUCCESS: changed-body mutation"
  exit 1
else
  echo "EXPECTED FAILURE: changed-body mutation"
fi
