#!/usr/bin/env bash
set -uo pipefail

echo '$ PYTHONPATH=/reference python3 /audit-output/evidence/05_stage4_preflight.py'
PYTHONPATH=/reference python3 /audit-output/evidence/05_stage4_preflight.py
