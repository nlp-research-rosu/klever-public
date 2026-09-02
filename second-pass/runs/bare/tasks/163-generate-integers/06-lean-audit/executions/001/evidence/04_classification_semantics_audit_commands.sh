#!/usr/bin/env bash
set -uo pipefail
trap 'rc=$?; printf "\nEXIT_CODE=%s\n" "$rc"' EXIT

python3 /audit-output/evidence/04_classification_semantics_audit.py
