#!/usr/bin/env bash
set -euo pipefail
trap 'rc=$?; echo "EXIT_STATUS=$rc"' EXIT

source_dir=/tmp/audit-work/11-string-xor/source
definition=/tmp/audit-work/11-string-xor/build/verification-kompiled

echo 'COMMAND: bash /audit-output/evidence/04_pinning.sh'

echo 'COMMAND: kast submitted solution.mpy to expanded KORE'
kast \
  --definition "$definition" \
  --module MPY-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  "$source_dir/solution.mpy" \
  > /tmp/audit-work/11-string-xor/solution.kore

echo 'COMMAND: kast solutionProgram macro to expanded KORE'
kast \
  --definition "$definition" \
  --module XOR-VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  --expression solutionProgram \
  > /tmp/audit-work/11-string-xor/macro.kore

echo 'COMMAND: cmp expanded submitted term and expanded claim macro'
cmp \
  /tmp/audit-work/11-string-xor/solution.kore \
  /tmp/audit-work/11-string-xor/macro.kore
sha256sum \
  /tmp/audit-work/11-string-xor/solution.kore \
  /tmp/audit-work/11-string-xor/macro.kore
echo 'constructor_level_program_identity=true'

cd "$source_dir"
echo 'COMMAND: kprove spec-ground-witness.k --spec-module XOR-GROUND-WITNESS --definition /tmp/audit-work/11-string-xor/build/verification-kompiled --output pretty'
kprove spec-ground-witness.k \
  --spec-module XOR-GROUND-WITNESS \
  --definition "$definition" \
  --output pretty

echo 'COMMAND: compare satisfying witness against both Python implementations'
python3 - <<'PY'
import importlib.util
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.string_xor


canonical = load("canonical_witness", "../reference/canonical.py")
candidate = load("candidate_witness", "solution.py")
a = "010"  # segment(3, seed(2)): least-significant bits 0,1,0
b = "110"  # segment(3, seed(3)): least-significant bits 1,1,0
expected = "100"
assert canonical(a, b) == expected
assert candidate(a, b) == expected
print(f"witness_a={a}")
print(f"witness_b={b}")
print(f"canonical={canonical(a, b)}")
print(f"candidate={candidate(a, b)}")
print("claimed_ground_result=100")
PY

echo 'COMMAND: kprove spec-body-sensitivity.k --spec-module XOR-BODY-SENSITIVITY --definition /tmp/audit-work/11-string-xor/build/verification-kompiled --output pretty'
set +e
kprove spec-body-sensitivity.k \
  --spec-module XOR-BODY-SENSITIVITY \
  --definition "$definition" \
  --output pretty \
  > /tmp/audit-work/11-string-xor/body-sensitivity.out 2>&1
body_status=$?
set -e
cat /tmp/audit-work/11-string-xor/body-sensitivity.out
echo "BODY_SENSITIVITY_EXIT_STATUS=$body_status"
test "$body_status" -ne 0
grep -F 'WarnStuckClaimState' /tmp/audit-work/11-string-xor/body-sensitivity.out > /dev/null
echo 'body_mutation_rejected_for_expected_obligation=true'
