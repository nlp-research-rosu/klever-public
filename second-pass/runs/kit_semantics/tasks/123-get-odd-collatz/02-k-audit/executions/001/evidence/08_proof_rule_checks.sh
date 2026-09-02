#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

python3 /audit-output/evidence/08_proof_rule_checks.py
printf 'proof_rule_checks_exit=%s\n' "$?"
