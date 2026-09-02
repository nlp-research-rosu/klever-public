#!/usr/bin/env bash
set -uo pipefail
trap 'rc=$?; printf "\nEXIT_CODE=%s\n" "$rc"' EXIT

PYTHONPATH=/reference python3 \
  /audit-output/evidence/05_check_generation.py
