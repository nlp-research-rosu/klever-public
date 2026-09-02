#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

python3 /audit-output/evidence/09_rule_decisions.py
printf 'rule_decisions_exit=%s\n' "$?"
wc -lc /audit-output/evidence/09_rule_decisions.tsv
sha256sum /audit-output/evidence/09_rule_decisions.tsv
