#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Recreate the translated artifact from the submitted implementation.
python3 py2mpy.py solution.py > solution.mpy

# Keep the program term in the symbolic claim tied to the generated artifact.
python3 - <<'PY'
import re
from pathlib import Path

translated = re.sub(r"\s+", "", Path("solution.mpy").read_text())
specification = Path("spec.k").read_text()
match = re.search(r"<k>\s*(Module\(.*\))\s*~>\s*invoke\(", specification, re.S)
assert match is not None, "could not find the claimed program term in spec.k"
claimed = re.sub(r"\s+", "", match.group(1))
assert claimed == translated, "spec.k program term differs from solution.mpy"
PY

# Compile the semantics together with the mathematical specification helper.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Execute all examples from prompt.py using the translated program itself.
krun solution.mpy --definition verification-kompiled -cFUNCTION='"sum_to_n"' -cARG=30
krun solution.mpy --definition verification-kompiled -cFUNCTION='"sum_to_n"' -cARG=100
krun solution.mpy --definition verification-kompiled -cFUNCTION='"sum_to_n"' -cARG=5
krun solution.mpy --definition verification-kompiled -cFUNCTION='"sum_to_n"' -cARG=10
krun solution.mpy --definition verification-kompiled -cFUNCTION='"sum_to_n"' -cARG=1

# Prove the symbolic claim for every natural-number input N.
kprove spec.k --definition verification-kompiled --spec-module SPEC
