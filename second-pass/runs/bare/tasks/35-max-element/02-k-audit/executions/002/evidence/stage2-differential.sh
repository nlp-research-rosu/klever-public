#!/usr/bin/env bash
set -euo pipefail
set -x

export PYTHONDONTWRITEBYTECODE=1
python3 /audit-output/evidence/differential_test.py
