#!/usr/bin/env bash
set -euo pipefail

# Regenerate the submitted constructor term from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Ensure the concrete smoke program embeds exactly the submitted definitions.
python3 - <<'PY'
import ast

with open("solution.py", encoding="utf-8") as source_file:
    solution = ast.parse(source_file.read())
with open("concrete_tests.py", encoding="utf-8") as tests_file:
    tests = ast.parse(tests_file.read())

embedded = ast.Module(
    body=tests.body[:len(solution.body)],
    type_ignores=[],
)
assert ast.dump(embedded) == ast.dump(solution)
PY

# Exercise the real keyed-sort implementation in the concrete LLVM semantics.
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Prove all claims against MPY without importing the concrete-only sort rules.
kompile verification.k \
  --backend haskell \
  --main-module ORDER-BY-POINTS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module ORDER-BY-POINTS-SPEC
