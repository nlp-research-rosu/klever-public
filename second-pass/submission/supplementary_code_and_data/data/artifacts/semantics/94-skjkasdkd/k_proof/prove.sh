#!/usr/bin/env bash
set -euo pipefail

# The required translation artifact.
python3 py2mpy.py solution.py > solution.mpy

# Concrete LLVM execution: the six prompt examples and four edge cases are
# assertions in concrete-tests.py.
python3 - <<'PY'
import ast

def first_function(path):
    with open(path, encoding="utf-8") as source:
        tree = ast.parse(source.read(), filename=path)
    return next(node for node in tree.body if isinstance(node, ast.FunctionDef))

assert ast.dump(first_function("solution.py")) == ast.dump(first_function("concrete-tests.py"))
PY
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# Symbolic definition: VERIFICATION imports MPY, never MPY-CONCRETE.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled \
  -I .

# Prove each invariant before admitting it as a trusted dependency of a later
# modular proof command.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.prime-loop \
  --output pretty

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.digit-loop \
  --output pretty

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
  --trusted SPEC.prime-loop,SPEC.digit-loop \
  --output pretty

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
  --trusted SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
  --output pretty

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.main-correct,SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
  --trusted SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
  --output pretty
