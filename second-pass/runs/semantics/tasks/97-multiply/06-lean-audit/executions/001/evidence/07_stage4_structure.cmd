#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' \
  'COMMAND: PYTHONPATH=/reference python3 /audit-output/evidence/07_stage4_structure.py'
PYTHONPATH=/reference python3 \
  /audit-output/evidence/07_stage4_structure.py
printf '%s\n' 'COMMAND: render obligation map and target-bearing generated modules'
python3 -m json.tool --sort-keys \
  /reference/klean-generation/generated/obligation-map.json
nl -ba /reference/klean-generation/generated/Klean97Multiply.lean
nl -ba /reference/klean-generation/generated/Klean97Multiply/Lemmas.lean
