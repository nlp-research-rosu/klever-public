#!/usr/bin/env bash
set -o xtrace
python3 /audit-output/evidence/inspect_generation_evidence.py
status=$?
printf 'EXIT_STATUS=%s\n' "$status"
exit "$status"
