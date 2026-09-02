#!/usr/bin/env bash
set +e
printf '$ python3 /audit-output/evidence/provenance_summary.py\n'
python3 /audit-output/evidence/provenance_summary.py
printf 'EXIT: %d\n' "$?"
