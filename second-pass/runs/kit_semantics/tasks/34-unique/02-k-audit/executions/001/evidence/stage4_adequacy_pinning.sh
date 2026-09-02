#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage4_adequacy_pinning.log
scratch=/tmp/audit-work/review-34-unique
exec >"$log" 2>&1

run() {
  echo "COMMAND: $*"
  "$@"
  status=$?
  echo "EXIT: $status"
  return "$status"
}

echo "STAGE 4 ADEQUACY AND REAL-PROGRAM PINNING"
run python3 /audit-output/evidence/stage4_pinning.py || exit $?

echo "COMMAND: copy reviewer witness into scratch for relative K requires"
cp /audit-output/evidence/stage4_witness.k "$scratch/stage4_witness.k"
status=$?
echo "EXIT: $status"

run kprove "$scratch/stage4_witness.k" \
  --definition "$scratch/audit-verification-base-kompiled" \
  --spec-module AUDIT-MEMBER-WITNESS || exit $?

run kprove "$scratch/stage4_witness.k" \
  --definition "$scratch/audit-verification-member-kompiled" \
  --spec-module AUDIT-LOOP-WITNESS || exit $?

run kprove "$scratch/stage4_witness.k" \
  --definition "$scratch/audit-verification-kompiled" \
  --spec-module AUDIT-ENTRY-WITNESS || exit $?

echo "COMMAND: execute both Python implementations on satisfying entry input [2,1,2]"
(
  cd "$scratch" || exit 99
  python3 - <<'PY'
import importlib.util
from pathlib import Path

def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique

candidate = load("solution.py", "stage4_candidate")
canonical = load("trusted-canonical.py", "stage4_canonical")
witness = [2, 1, 2]
print("witness", witness)
print("candidate", candidate(witness.copy()))
print("canonical", canonical(witness.copy()))
assert candidate(witness.copy()) == [1, 2]
assert canonical(witness.copy()) == [1, 2]
PY
)
status=$?
echo "EXIT: $status"
