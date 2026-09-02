#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/case91
overall=0

printf 'SUPPLIED_MODEL_RULE: methods.k:85-86 isWSC(C) iff C in {32,9,10,13}\n'
printf 'DIVERGENCE_WITNESS: input=\"I\\\\vwork\" (vertical-tab code 11)\n'

printf 'COMMAND: cp /audit-output/evidence/stage7-model-boundary.py %s/stage7-model-boundary.py\n' "$scratch"
cp /audit-output/evidence/stage7-model-boundary.py "$scratch/stage7-model-boundary.py"
copy_ec=$?
printf 'COPY_EXIT=%d\n' "$copy_ec"
if [[ $copy_ec -ne 0 ]]; then overall=1; fi

printf 'COMMAND: cd %s && python3 py2mpy.py stage7-model-boundary.py > stage7-model-boundary.mpy\n' "$scratch"
(
  cd "$scratch"
  python3 py2mpy.py stage7-model-boundary.py > stage7-model-boundary.mpy
)
translate_ec=$?
printf 'TRANSLATOR_EXIT=%d\n' "$translate_ec"
if [[ $translate_ec -ne 0 ]]; then overall=1; fi

printf 'COMMAND: cd %s && krun stage7-model-boundary.mpy --definition audit-runtime-kompiled\n' "$scratch"
(
  cd "$scratch"
  krun stage7-model-boundary.mpy --definition audit-runtime-kompiled
)
krun_ec=$?
printf 'KRUN_EXIT=%d\n' "$krun_ec"
if [[ $krun_ec -ne 0 ]]; then overall=1; fi

printf 'COMMAND: python3 - (load candidate and canonical; evaluate vertical-tab witness)\n'
python3 - <<'PY'
import importlib.util
from pathlib import Path

root = Path("/tmp/audit-work/case91")

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored

candidate = load(root / "solution.py", "stage7_candidate")
canonical = load(root / "canonical.py", "stage7_canonical")
value = "I\vwork"
print(f"vertical_tab_isspace={value[1].isspace()}")
print(f"candidate_cpython={candidate(value)}")
print(f"canonical_helper={canonical(value)}")
PY
python_ec=$?
printf 'PYTHON_EXIT=%d\n' "$python_ec"
if [[ $python_ec -ne 0 ]]; then overall=1; fi

printf 'FINAL_STATUS=%d\n' "$overall"
exit "$overall"
