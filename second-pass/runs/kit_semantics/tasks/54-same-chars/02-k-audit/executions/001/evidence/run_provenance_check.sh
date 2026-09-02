#!/usr/bin/env bash
set -o xtrace
python3 /audit-output/evidence/provenance_check.py
status=$?
printf 'EXIT_STATUS=%s\n' "$status"
exit "$status"
