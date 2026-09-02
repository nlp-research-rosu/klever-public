#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

expected_mpy_sha256=fc50d53a7c774d8a12149ad71f3ab5988849f3623c8c83d72d4ed772e3c8f630
actual_mpy_sha256="$(sha256sum solution.mpy | cut -d' ' -f1)"
test "$actual_mpy_sha256" = "$expected_mpy_sha256"
printf 'solution.mpy identity: %s\n' "$actual_mpy_sha256"

python3 - <<'PY'
import ast
from pathlib import Path

solution = ast.parse(Path("solution.py").read_text()).body[0]
smoke = ast.parse(Path("smoke.py").read_text()).body[0]
assert ast.dump(solution, include_attributes=False) == ast.dump(
    smoke, include_attributes=False
)
print("smoke-function-identity: PASS")
PY

python3 smoke.py
python3 differential.py
python3 py2mpy.py smoke.py > smoke.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY > vacuity.log 2>&1
vacuity_status=$?
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION > body-mutation.log 2>&1
body_mutation_status=$?
set -e

if [[ "$vacuity_status" -eq 0 ]]; then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
fi
if [[ "$body_mutation_status" -eq 0 ]]; then
  echo "ERROR: mutated body unexpectedly proved the original claim"
  exit 1
fi

printf 'vacuity mutation: EXPECTED FAILURE (exit %s)\n' "$vacuity_status"
printf 'body mutation: EXPECTED FAILURE (exit %s)\n' "$body_mutation_status"
