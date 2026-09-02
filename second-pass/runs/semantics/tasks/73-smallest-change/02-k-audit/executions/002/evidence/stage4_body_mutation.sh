#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/73-smallest-change
cd "$scratch"

echo 'TRANSLATE_COMMAND: python3 trusted-py2mpy.py solution-body-mutant.py > solution-body-mutant.mpy'
python3 trusted-py2mpy.py solution-body-mutant.py > solution-body-mutant.mpy

echo 'TRANSLATE_COMMAND: python3 trusted-py2mpy.py body-mutant-concrete.py > body-mutant-concrete.mpy'
python3 trusted-py2mpy.py body-mutant-concrete.py > body-mutant-concrete.mpy

echo 'PYTHON_COMMAND: import solution-body-mutant.py and evaluate smallest_change([])'
python3 -c 'import importlib.util; p="solution-body-mutant.py"; s=importlib.util.spec_from_file_location("body_mutant", p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print("python_mutated_result_empty=" + str(m.smallest_change([])))'

echo 'KRUN_COMMAND: krun body-mutant-concrete.mpy --definition audit-runtime-kompiled'
krun body-mutant-concrete.mpy --definition audit-runtime-kompiled
