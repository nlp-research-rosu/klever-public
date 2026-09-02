#!/usr/bin/env bash
set -uo pipefail

python3 /audit-output/evidence/provenance/provenance_check.py
status=$?
printf 'EXIT_STATUS=%s\n' "$status"
exit "$status"
