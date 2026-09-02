#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/case91
overall=0

printf 'COMMAND: cp /audit-output/evidence/stage4-witness-spec.k %s/stage4-witness-spec.k\n' "$scratch"
cp /audit-output/evidence/stage4-witness-spec.k "$scratch/stage4-witness-spec.k"
copy_ec=$?
printf 'COPY_EXIT=%d\n' "$copy_ec"
if [[ $copy_ec -ne 0 ]]; then overall=1; fi

printf 'COMMAND: cd %s && kprove stage4-witness-spec.k --definition audit-verification-kompiled --spec-module STAGE4-WITNESS-SPEC\n' "$scratch"
(
  cd "$scratch"
  kprove stage4-witness-spec.k \
    --definition audit-verification-kompiled \
    --spec-module STAGE4-WITNESS-SPEC
)
kprove_ec=$?
printf 'KPROVE_EXIT=%d\n' "$kprove_ec"
if [[ $kprove_ec -ne 0 ]]; then overall=1; fi

printf 'COMMAND: python3 - (load candidate and canonical; evaluate empty string and \"I work\")\n'
python3 - <<'PY'
import importlib.util
from pathlib import Path

root = Path("/tmp/audit-work/case91")

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored

candidate = load(root / "solution.py", "stage4_candidate")
canonical = load(root / "canonical.py", "stage4_canonical")
for value in ("", "I work"):
    print(
        f"input={value!r} candidate={candidate(value)} "
        f"canonical={canonical(value)}"
    )
PY
python_ec=$?
printf 'PYTHON_EXIT=%d\n' "$python_ec"
if [[ $python_ec -ne 0 ]]; then overall=1; fi

printf 'FINAL_STATUS=%d\n' "$overall"
exit "$overall"
