#!/usr/bin/env bash
set -u

probe_py=/audit-output/evidence/get_boundary_probe.py
probe_mpy=/tmp/audit-work/135-can-arrange/build/get_boundary_probe.mpy
definition=/tmp/audit-work/135-can-arrange/build/concrete-kompiled

printf 'INPUT: []\n'
printf 'PYTHON COMMAND: python3 -c (load probe and call can_arrange([]))\n'
python3 - "$probe_py" <<'PY'
import importlib.util
import sys

path = sys.argv[1]
spec = importlib.util.spec_from_file_location("get_boundary_probe", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
try:
    result = module.can_arrange([])
except BaseException as err:
    print(f"PYTHON OBSERVATION: exception {type(err).__name__}: {err}")
else:
    print(f"PYTHON OBSERVATION: return {result!r}")
PY
python_status=$?
printf 'PYTHON EXIT: %d\n' "$python_status"

printf 'TRANSLATE COMMAND: python3 /reference/py2mpy.py %s > %s\n' "$probe_py" "$probe_mpy"
python3 /reference/py2mpy.py "$probe_py" > "$probe_mpy"
translate_status=$?
printf 'TRANSLATE EXIT: %d\n' "$translate_status"

printf "K COMMAND: krun %s '-cARGS=arrayVal(seq(),0,0)' --definition %s\n" "$probe_mpy" "$definition"
krun "$probe_mpy" "-cARGS=arrayVal(seq(),0,0)" --definition "$definition"
k_status=$?
printf 'K EXIT: %d\n' "$k_status"

if (( python_status == 0 && translate_status == 0 && k_status == 0 )); then
  exit 0
fi
exit 1
