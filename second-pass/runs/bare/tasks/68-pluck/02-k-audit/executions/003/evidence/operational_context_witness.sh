#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/68-pluck-audit

echo '$ python3 trusted-py2mpy.py shadow-enumerate.py > shadow-enumerate.mpy'
python3 "$scratch/trusted-py2mpy.py" "$scratch/shadow-enumerate.py" \
  > "$scratch/shadow-enumerate.mpy"
translate_status=$?
echo "shadow translator exit=$translate_status"

echo '$ Python shadow-enumerate.pluck([2])'
python3 - "$scratch/shadow-enumerate.py" <<'PY'
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("shadow_enumerate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
result = module.pluck([2])
print(f"Python result={result}")
raise SystemExit(0 if result == [] else 1)
PY
python_status=$?
echo "Python shadow witness exit=$python_status"

echo '$ krun shadow-enumerate.mpy --definition concrete-audit-kompiled -cARGS=VList(2)'
k_output=$(
  krun "$scratch/shadow-enumerate.mpy" \
    --definition "$scratch/concrete-audit-kompiled" \
    -cARGS='VList(2)' 2>&1
)
k_status=$?
printf '%s\n' "$k_output"
echo "K shadow witness krun exit=$k_status"
grep -Fq '    VList ( 2 , 0 , .Ints )' <<<"$k_output"
k_wrong_result=$?
echo "K result [2,0] check exit=$k_wrong_result"

overall=$((translate_status || python_status || k_status || k_wrong_result))
echo "operational-context witness aggregate exit=$overall"
exit "$overall"
