#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

python3 /audit-output/evidence/07_pinning_and_witness.py
printf 'pinning_and_witness_exit=%s\n' "$?"
