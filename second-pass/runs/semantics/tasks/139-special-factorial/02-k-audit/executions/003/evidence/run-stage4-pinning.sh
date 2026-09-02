#!/usr/bin/env bash
set -uo pipefail
set -x

export PATH=/home/agent/.nix-profile/bin:$PATH
cd /tmp/audit-work/case

python3 /audit-output/evidence/check_program_pinning.py
pinning_status=$?
printf 'PINNING_CHECK_EXIT=%s\n' "$pinning_status"

python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.special_factorial

candidate = load("candidate", "/tmp/audit-work/case/solution.py")
canonical = load("canonical", "/reference/canonical.py")
for n in (1, 3, 4, 6):
    factorial = 1
    product = 1
    for i in range(1, n + 1):
        factorial *= i
        product *= factorial
    print(
        f"N={n} entry_precondition={n > 0} "
        f"claimed_specialFactorial={product} "
        f"candidate={candidate(n)} canonical={canonical(n)} "
        f"loop_exit_factorial={factorial} loop_exit_i={n + 1}"
    )
    assert candidate(n) == canonical(n) == product
PY
ground_status=$?
printf 'GROUND_SUBSTITUTION_EXIT=%s\n' "$ground_status"

kprove spec-body-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --output pretty
mutation_status=$?
printf 'BODY_MUTATION_KPROVE_EXIT=%s\n' "$mutation_status"

if [[ "$pinning_status" -ne 0 || "$ground_status" -ne 0 ]]; then
  exit 1
fi
if [[ "$mutation_status" -eq 0 ]]; then
  exit 1
fi
exit 0
