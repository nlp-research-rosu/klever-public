#!/usr/bin/env bash
set -uo pipefail
set -x

scratch=/tmp/audit-work/candidate-src
raw=/tmp/audit-work/stage6-raw
mutation=/audit-output/evidence/spec-fresh-vacuity.k
mkdir -p "$raw"
overall=0

python3 - <<'PY'
import importlib.util
from pathlib import Path

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted

case = [0, 1]
canonical = load(Path("/reference/canonical.py"), "fresh_vac_canonical")
generated = load(Path("/tmp/audit-work/candidate-src/solution.py"), "fresh_vac_generated")
print(
    f"witness={case} nonNegativeInts=True "
    f"canonical={canonical(case)} generated={generated(case)} "
    "mutated_destination=False"
)
if canonical(case) is not True or generated(case) is not True:
    raise SystemExit(1)
PY
witness_status=$?
printf 'witness_check_status=%s\n' "$witness_status"
if (( witness_status != 0 )); then
  overall=1
fi

kprove "$mutation" \
  --definition "$scratch/audit-verification-kompiled" \
  --spec-module AUDIT-FRESH-VACUITY \
  --dry-run \
  > "$raw/dry-run.log" 2>&1
dry_status=$?
printf '%s\n' \
  'COMMAND: kprove /audit-output/evidence/spec-fresh-vacuity.k --definition /tmp/audit-work/candidate-src/audit-verification-kompiled --spec-module AUDIT-FRESH-VACUITY --dry-run'
printf 'EXIT[fresh-mutation-dry-run]=%s\n' "$dry_status"
sed -n '1,100p' "$raw/dry-run.log"
if (( dry_status != 0 )); then
  overall=1
fi

kprove "$mutation" \
  --definition "$scratch/audit-verification-kompiled" \
  --spec-module AUDIT-FRESH-VACUITY \
  > "$raw/kprove.log" 2>&1
prove_status=$?
printf '%s\n' \
  'COMMAND: kprove /audit-output/evidence/spec-fresh-vacuity.k --definition /tmp/audit-work/candidate-src/audit-verification-kompiled --spec-module AUDIT-FRESH-VACUITY'
printf 'EXIT[fresh-mutation-proof]=%s (nonzero expected)\n' "$prove_status"
sed -n '1,220p' "$raw/kprove.log"

if (( prove_status == 0 )); then
  printf '%s\n' 'ERROR: false mutation unexpectedly proved'
  overall=1
fi
if ! grep -q 'WarnStuckClaimState' "$raw/kprove.log"; then
  printf '%s\n' 'ERROR: expected unmet-obligation residual was absent'
  overall=1
fi
if ! grep -q 'false' "$raw/kprove.log"; then
  printf '%s\n' 'ERROR: residual did not expose the false result obligation'
  overall=1
fi

printf 'STAGE6_OVERALL=%s\n' "$overall"
exit "$overall"
