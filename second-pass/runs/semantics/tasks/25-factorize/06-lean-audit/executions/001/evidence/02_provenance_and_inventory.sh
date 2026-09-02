#!/usr/bin/env bash
set -uo pipefail

echo '$ PYTHONPATH=/reference python3 /audit-output/evidence/02_provenance_and_inventory.py'
PYTHONPATH=/reference python3 /audit-output/evidence/02_provenance_and_inventory.py
