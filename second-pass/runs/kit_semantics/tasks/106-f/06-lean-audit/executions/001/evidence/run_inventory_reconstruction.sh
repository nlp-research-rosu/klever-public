#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

export PYTHONPATH=/reference
python3 /audit-output/evidence/reconstruct_inventory.py
