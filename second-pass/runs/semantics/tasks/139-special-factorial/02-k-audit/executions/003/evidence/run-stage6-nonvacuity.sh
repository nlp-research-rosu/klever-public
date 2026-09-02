#!/usr/bin/env bash
set -uo pipefail
set -x

export PATH=/home/agent/.nix-profile/bin:$PATH
cd /tmp/audit-work/case

python3 - <<'PY'
from importlib.util import module_from_spec, spec_from_file_location

def load(name, path):
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.special_factorial

candidate = load("candidate", "/tmp/audit-work/case/solution.py")
canonical = load("canonical", "/reference/canonical.py")
n = 1
actual_candidate = candidate(n)
actual_canonical = canonical(n)
mutated_required = actual_canonical + 1
print(
    f"witness N={n} precondition={n > 0} "
    f"candidate={actual_candidate} canonical={actual_canonical} "
    f"mutated_required={mutated_required} "
    f"mutation_false={actual_candidate != mutated_required}"
)
assert n > 0
assert actual_candidate == actual_canonical == 1
assert actual_candidate != mutated_required
PY
witness_status=$?
printf 'WITNESS_EXIT=%s\n' "$witness_status"

kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
dry_run_status=$?
printf 'MUTATION_DRY_RUN_EXIT=%s\n' "$dry_run_status"

kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --output pretty
proof_status=$?
printf 'MUTATION_KPROVE_EXIT=%s\n' "$proof_status"

if [[ "$witness_status" -ne 0 || "$dry_run_status" -ne 0 ]]; then
  exit 1
fi
if [[ "$proof_status" -eq 0 ]]; then
  exit 1
fi
exit 0
