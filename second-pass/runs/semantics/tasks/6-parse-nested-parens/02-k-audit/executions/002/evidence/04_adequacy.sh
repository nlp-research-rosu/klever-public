#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
export PATH="/home/agent/.nix-profile/bin:$PATH"

echo 'COMMAND: python3 /audit-output/evidence/04_pinning.py'
python3 /audit-output/evidence/04_pinning.py
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo 'COMMAND: kprove spec-ground.k --definition audit-verification-kompiled --spec-module SPEC-GROUND --output pretty'
(
  cd "$work" || exit 1
  kprove spec-ground.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC-GROUND \
    --output pretty
)
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo 'COMMAND: compare satisfying witness with trusted and generated Python'
PYTHONPATH="/reference:$work" python3 - <<'PY'
import importlib.util
from pathlib import Path

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_nested_parens

canonical = load("canonical_witness", Path("/reference/canonical.py"))
generated = load("generated_witness", Path("/tmp/audit-work/reconstruction/solution.py"))
witness = "(()()) ()"
expected = [2, 1]
print(f"witness={witness!r}")
print(f"explicit_claim_result={expected}")
print(f"trusted_canonical_result={canonical(witness)}")
print(f"generated_python_result={generated(witness)}")
assert canonical(witness) == expected
assert generated(witness) == expected
print("GROUND_THREE_WAY_COMPARISON=PASS")
PY
status=$?
echo "EXIT_STATUS: $status"
exit "$status"
