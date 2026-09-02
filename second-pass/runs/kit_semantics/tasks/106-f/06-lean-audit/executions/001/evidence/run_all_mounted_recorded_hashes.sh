#!/usr/bin/env bash
set -u
export PYTHONPATH=/reference
python3 /audit-output/evidence/check_all_mounted_recorded_hashes.py
