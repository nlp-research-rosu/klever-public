#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/153-strongest-extension

echo '$ krun solution.mpy --definition semantic-kompiled -cCLASS="C" -cEXTENSIONS=strVal("a");strVal("éé")'
krun "$scratch/solution.mpy" --definition "$scratch/semantic-kompiled" \
  -cCLASS='"C"' -cEXTENSIONS='strVal("a");strVal("éé")'
k_status=$?
echo "exit_status=$k_status"

echo '$ python3 unicode-lower-oracle.py canonical.py solution.py'
python3 /audit-output/evidence/stage5/unicode-lower-oracle.py \
  "$scratch/canonical.py" "$scratch/solution.py"
python_status=$?
echo "exit_status=$python_status"

if [[ $k_status -ne 0 || $python_status -ne 0 ]]; then
  exit 1
fi
