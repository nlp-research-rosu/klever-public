#!/usr/bin/env bash
set -u

work=/tmp/audit-work/rebuild
mutation=spec-vacuity-audit.k
status=0

echo '$ kprove spec-vacuity-audit.k --definition proof-kompiled --spec-module FIBFIB-SPEC-VACUITY-AUDIT --dry-run'
(
  cd "$work" || exit 1
  kprove "$mutation" \
    --definition proof-kompiled \
    --spec-module FIBFIB-SPEC-VACUITY-AUDIT \
    --dry-run
)
dry_rc=$?
echo "dry_run_exit=$dry_rc"
if (( dry_rc != 0 )); then
  status=1
fi

echo '$ kprove spec-vacuity-audit.k --definition proof-kompiled --spec-module FIBFIB-SPEC-VACUITY-AUDIT'
(
  cd "$work" || exit 1
  kprove "$mutation" \
    --definition proof-kompiled \
    --spec-module FIBFIB-SPEC-VACUITY-AUDIT
)
prove_rc=$?
echo "proof_exit=$prove_rc (expected nonzero)"
if (( prove_rc == 0 )); then
  status=1
fi

echo '$ demonstrate a satisfying false witness in both Python implementations'
python3 - <<'PY'
import importlib.util
from pathlib import Path

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fibfib

canonical = load("canonical_false_witness", Path("/tmp/audit-work/reference-src/canonical.py"))
generated = load("generated_false_witness", Path("/tmp/audit-work/candidate-src/solution.py"))
n = 5
real = canonical(n)
candidate = generated(n)
mutated = real + 1
print(f"N={n} satisfies_0_le_N={0 <= n}")
print(f"canonical={real} generated={candidate} mutated_obligation={mutated}")
print(f"mutation_is_false={real == candidate and real != mutated}")
if not (real == candidate and real != mutated):
    raise SystemExit(1)
PY
witness_rc=$?
echo "witness_exit=$witness_rc"
if (( witness_rc != 0 )); then
  status=1
fi

echo '$ preserve mutation below /audit-output/evidence'
cp --no-dereference \
  "$work/$mutation" \
  /audit-output/evidence/spec-vacuity-audit.k

echo "overall_exit=$status"
exit "$status"
