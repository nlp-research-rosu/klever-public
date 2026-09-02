#!/usr/bin/env bash
set -uo pipefail
set -x

python3 /audit-output/evidence/claim_witnesses.py
rc=$?
printf 'claim_witness_comparison_exit=%d\n' "$rc"
exit "$rc"
