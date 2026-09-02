#!/usr/bin/env bash
set -euo pipefail

inventory=/audit-output/evidence/k-rule-inventory.tsv

printf '%s\n' '== Candidate-local entries =='
awk -F '\t' 'NR == 1 || $2 ~ /^candidate-/' "$inventory"

printf '%s\n' '== Opaque declarations =='
awk -F '\t' 'NR == 1 || $7 ~ /no-evaluators|symbol\(/' "$inventory"

printf '%s\n' '== Simplification / functional entries =='
awk -F '\t' 'NR == 1 || $7 ~ /simplification|functional/' "$inventory"

printf '%s\n' '== Priority entries =='
awk -F '\t' 'NR == 1 || $7 ~ /priority\(/' "$inventory"
