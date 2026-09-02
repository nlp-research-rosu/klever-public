#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/62-derivative
cp --no-dereference /audit-output/evidence/stage5_bridge_probe.py "$scratch/stage5_bridge_probe.py"
cd "$scratch" || exit 70

python3 py2mpy.py stage5_bridge_probe.py > stage5_bridge_probe.mpy
translate_status=$?
printf 'TRANSLATE_EXIT_STATUS: %d\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

for definition in runtime-kompiled verification-runtime-kompiled
do
  printf 'DEFINITION: %s\n' "$definition"
  timeout 180 krun stage5_bridge_probe.mpy --definition "$definition"
  status=$?
  printf 'KRUN_EXIT_STATUS: %d\n' "$status"
  if (( status != 0 )); then
    exit "$status"
  fi
done
