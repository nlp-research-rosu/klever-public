#!/usr/bin/env bash
set -uo pipefail

run_checked() {
  echo "+ $*"
  "$@"
  local status=$?
  echo "EXIT: $status"
  if [[ $status -ne 0 ]]; then
    exit "$status"
  fi
}

cd /tmp/audit-work/reconstruction
cp -a /audit-output/evidence/stage7_concrete_smoke.py stage7_concrete_smoke.py
echo "+ python3 py2mpy.py stage7_concrete_smoke.py > stage7_concrete_smoke.mpy"
python3 py2mpy.py stage7_concrete_smoke.py > stage7_concrete_smoke.mpy
status=$?
echo "EXIT: $status"
if [[ $status -ne 0 ]]; then
  exit "$status"
fi
run_checked krun stage7_concrete_smoke.mpy \
  --definition auditor-runtime-kompiled
