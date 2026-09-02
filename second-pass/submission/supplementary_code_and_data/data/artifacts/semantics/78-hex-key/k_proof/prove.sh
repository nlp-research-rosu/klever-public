#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy

# The concrete test program must contain the submitted implementation verbatim.
python3 - <<'PY'
from pathlib import Path

solution = Path("solution.py").read_text(encoding="utf-8").rstrip()
tests = Path("concrete_tests.py").read_text(encoding="utf-8")
assert tests.startswith(solution + "\n\n"), \
    "concrete_tests.py does not begin with the exact solution.py implementation"
PY
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Concrete LLVM execution of the prompt examples.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled | tee krun.out
grep -A1 '<k>' krun.out | tail -n 1 | grep -Eq '^[[:space:]]*\.K[[:space:]]*$'
grep -A1 '<exit-code>' krun.out | tail -n 1 | grep -Eq '^[[:space:]]*0[[:space:]]*$'

# Symbolic definition and all-path proof of every claim in spec.k.
kompile verification.k \
  --backend haskell \
  --main-module HEX-KEY-VERIFICATION \
  --syntax-module HEX-KEY-VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module HEX-KEY-SPEC | tee kprove.out
grep -qx '#Top' kprove.out
