#!/usr/bin/env bash
set -uo pipefail

echo '$ PYTHONPATH=/reference python3 /audit-output/evidence/07_stage4_independent_gate.py'
PYTHONPATH=/reference python3 /audit-output/evidence/07_stage4_independent_gate.py

echo '$ rg -n "\b(targetStatement|Proof\\.final)\b" /reference/klean-generation/generated -g "*.lean"'
rg -n '\b(targetStatement|Proof\.final)\b' \
  /reference/klean-generation/generated \
  -g '*.lean'
rg_rc=$?
echo "exit_code=$rg_rc (1 means no matches)"

echo '$ find /reference/klean-generation/generated -maxdepth 2 -type f -printf "%P\n" | sort'
find /reference/klean-generation/generated \
  -maxdepth 2 \
  -type f \
  -printf '%P\n' \
  | sort

exit 0
