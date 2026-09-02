#!/usr/bin/env bash
set -u
export PYTHONPATH=/reference
python3 /audit-output/evidence/check_candidate_target_identity.py
