#!/usr/bin/env bash
set -euo pipefail
set -x

python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.bf

canonical = load("fresh_mutation_canonical", "/reference/canonical.py")
candidate = load("fresh_mutation_candidate", "/tmp/audit-work/rebuild/solution.py")
witness = ("Jupiter", "Neptune")
print("satisfying witness:", witness)
print("trusted canonical:", canonical(*witness))
print("candidate Python:", candidate(*witness))
print("mutated claimed result:", ("Saturn",))
assert canonical(*witness) == candidate(*witness) == ("Saturn", "Uranus")
assert canonical(*witness) != ("Saturn",)
PY

kprove audit-spec-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run

set +e
kprove audit-spec-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  > /tmp/audit-work/fresh-vacuity-proof-output.log 2>&1
mutation_rc=$?
set -e

cat /tmp/audit-work/fresh-vacuity-proof-output.log
echo "fresh false-postcondition kprove exit=$mutation_rc"
test "$mutation_rc" -ne 0
rg 'WarnStuckClaimState' /tmp/audit-work/fresh-vacuity-proof-output.log
rg 'tupleValue' /tmp/audit-work/fresh-vacuity-proof-output.log
rg '"Saturn"' /tmp/audit-work/fresh-vacuity-proof-output.log
rg '"Uranus"' /tmp/audit-work/fresh-vacuity-proof-output.log

if rg 'Parse error|Had [0-9]+ parsing errors' \
  /tmp/audit-work/fresh-vacuity-proof-output.log
then
  echo "ERROR: mutation failed for a parsing reason"
  exit 1
fi

echo "fresh non-vacuity mutation rejected on the expected unmet result obligation"
