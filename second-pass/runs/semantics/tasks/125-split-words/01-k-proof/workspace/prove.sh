#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# Build exactly the required concrete definition and exercise the submitted
# module plus a branch-covering assertion program.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
python3 - <<'PY'
import ast

with open("solution.py", encoding="utf-8") as stream:
    solution_def = ast.parse(stream.read()).body[0]
with open("concrete_tests.py", encoding="utf-8") as stream:
    test_def = ast.parse(stream.read()).body[0]
assert ast.dump(solution_def) == ast.dump(test_def)
PY
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy --definition runtime-kompiled

# Build the proof definition from MPY (not MPY-KRUN/MPY-CONCRETE) and prove all
# three exhaustive contract branches in one positive target-proof command.
kompile verification.k \
  --backend haskell \
  --main-module SPLIT-WORDS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled
