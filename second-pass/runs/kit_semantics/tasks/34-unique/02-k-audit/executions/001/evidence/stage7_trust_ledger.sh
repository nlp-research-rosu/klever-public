#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage7_trust_ledger.log
scratch=/tmp/audit-work/review-34-unique
exec >"$log" 2>&1

run() {
  echo "COMMAND: $*"
  "$@"
  status=$?
  echo "EXIT: $status"
  return "$status"
}

echo "STAGE 7 MODEL-GAP WITNESS FOR TRUST LEDGER"
echo "COMMAND: execute candidate and canonical Python functions on [True,1]"
(
  cd "$scratch" || exit 99
  python3 - <<'PY'
import importlib.util

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique

candidate = load("solution.py", "ledger_candidate")
canonical = load("trusted-canonical.py", "ledger_canonical")
case = [True, 1]
print("case", case)
print("candidate", candidate(case.copy()))
print("canonical", canonical(case.copy()))
assert candidate(case.copy()) == [True]
assert canonical(case.copy()) == [True]
PY
)
status=$?
echo "EXIT: $status"
if [[ "$status" -ne 0 ]]; then
  exit "$status"
fi

echo "COMMAND: trusted translation of reviewer concrete model-gap program"
python3 "$scratch/py2mpy.py" \
  /audit-output/evidence/stage7_model_gap_concrete.py \
  > "$scratch/stage7_model_gap_concrete.mpy"
status=$?
echo "EXIT: $status"
if [[ "$status" -ne 0 ]]; then
  exit "$status"
fi

echo "COMMAND: krun $scratch/stage7_model_gap_concrete.mpy --definition $scratch/audit-runtime-kompiled"
krun "$scratch/stage7_model_gap_concrete.mpy" \
  --definition "$scratch/audit-runtime-kompiled" 2>&1 | sed -n '1,180p'
status=${PIPESTATUS[0]}
echo "EXIT: $status"
if [[ "$status" -ne 0 ]]; then
  exit "$status"
fi

echo "COMMAND: copy reviewer symbolic witness into scratch"
cp /audit-output/evidence/stage7_model_gap.k "$scratch/stage7_model_gap.k"
status=$?
echo "EXIT: $status"
if [[ "$status" -ne 0 ]]; then
  exit "$status"
fi

run kprove "$scratch/stage7_model_gap.k" \
  --definition "$scratch/audit-verification-base-kompiled" \
  --spec-module AUDIT-SYMBOLIC-MODEL-GAP || exit $?

echo "COMMAND: kprove opposite CPython result under fixed symbolic semantics"
set +e
kprove "$scratch/stage7_model_gap.k" \
  --definition "$scratch/audit-verification-base-kompiled" \
  --spec-module AUDIT-SYMBOLIC-MODEL-OPPOSITE 2>&1 | sed -n '1,240p'
opposite_status=${PIPESTATUS[0]}
set -e
echo "EXIT: $opposite_status"
if [[ "$opposite_status" -eq 0 ]]; then
  echo "ERROR: symbolic model admitted the opposite result"
  exit 92
fi
echo "EXPECTED_MODEL_DIVERGENCE_FAILURE: $opposite_status"
