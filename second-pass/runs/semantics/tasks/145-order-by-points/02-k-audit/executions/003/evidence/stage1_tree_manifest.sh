#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/tree_manifest_check.py'
python3 /audit-output/evidence/tree_manifest_check.py
printf 'EXIT_STATUS: %s\n' "$?"
