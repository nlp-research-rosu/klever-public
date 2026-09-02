#!/usr/bin/env bash
set -uo pipefail
trap 'rc=$?; printf "\nEXIT_CODE=%s\n" "$rc"' EXIT

PYTHONPATH=/reference python3 \
  /audit-output/evidence/06_stage4_structural_audit.py

nl -ba \
  /reference/klean-generation/generated/Klean163GenerateIntegers.lean
nl -ba \
  /reference/klean-generation/generated/Klean163GenerateIntegers/Lemmas.lean
