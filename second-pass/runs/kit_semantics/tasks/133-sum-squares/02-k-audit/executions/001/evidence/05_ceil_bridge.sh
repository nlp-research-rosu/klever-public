#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/reconstruction
python3 /audit-output/evidence/05_ceil_bridge_generator.py
python3 ceil-bridge.py
python3 py2mpy.py ceil-bridge.py > ceil-bridge.mpy
krun ceil-bridge.mpy \
  --definition runtime-fresh-kompiled \
  > /audit-output/evidence/05-krun-ceil-bridge.log
bridge_status=$?
printf 'krun_ceil_bridge_exit=%s\n' "${bridge_status}"
rg -n '<k>|<exc>|<exit-code>' \
  /audit-output/evidence/05-krun-ceil-bridge.log
