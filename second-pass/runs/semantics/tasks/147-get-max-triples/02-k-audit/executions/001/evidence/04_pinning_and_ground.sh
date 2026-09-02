#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
overall=0
cd "$work" || exit 125

echo 'COMMAND: krun solution.mpy --definition audit-runtime-kompiled --output pretty'
krun solution.mpy --definition audit-runtime-kompiled --output pretty
status=$?
echo "EXIT_STATUS: $status"
if (( status != 0 )); then overall=1; fi

echo 'COMMAND: kprove /audit-output/evidence/04_ground_spec.k --definition audit-verification-kompiled --spec-module AUDIT-GROUND-SPEC --claims AUDIT-GROUND-SPEC.ground-n5 -I . --output pretty'
kprove /audit-output/evidence/04_ground_spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-GROUND-SPEC \
  --claims AUDIT-GROUND-SPEC.ground-n5 \
  -I . \
  --output pretty
status=$?
echo "EXIT_STATUS: $status"
if (( status != 0 )); then overall=1; fi

echo 'COMMAND: python3 -c (independent canonical/generated/summary comparison for n=5)'
python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_max_triples

canonical = load("canonical_ground", "/reference/canonical.py")
generated = load("generated_ground", "/tmp/audit-work/reconstruction/solution.py")
n = 5
zero_residues = (n + 1) // 3
choose_three = lambda c: c * (c - 1) * (c - 2) // 6
formal_summary = choose_three(zero_residues) + choose_three(n - zero_residues)
print(f"N {n}")
print(f"PRECONDITION_N_GT_0 {n > 0}")
print(f"CANONICAL {canonical(n)}")
print(f"GENERATED {generated(n)}")
print(f"FORMAL_TRIPLE_COUNT {formal_summary}")
assert canonical(n) == generated(n) == formal_summary == 1
PY
status=$?
echo "EXIT_STATUS: $status"
if (( status != 0 )); then overall=1; fi

exit "$overall"
