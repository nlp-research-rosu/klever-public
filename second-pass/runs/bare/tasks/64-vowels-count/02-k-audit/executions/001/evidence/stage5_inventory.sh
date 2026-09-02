#!/usr/bin/env bash
set -euo pipefail
set -x

for source in \
  /tmp/audit-work/candidate-src/semantic.k \
  /tmp/audit-work/candidate-src/verification.k \
  /tmp/audit-work/candidate-src/spec.k
do
  sha256sum "$source"
  nl -ba "$source"
done

rg -n \
  '^\s*(syntax|rule|claim|configuration)\b|\[(function|total|functional|macro|strict|seqstrict|simplification|concrete|owise|priority|anywhere)' \
  /tmp/audit-work/candidate-src/semantic.k \
  /tmp/audit-work/candidate-src/verification.k \
  /tmp/audit-work/candidate-src/spec.k

printf 'semantic_rules='
rg -c '^\s*rule\b' /tmp/audit-work/candidate-src/semantic.k
printf 'verification_rules='
rg -c '^\s*rule\b' /tmp/audit-work/candidate-src/verification.k
printf 'spec_claims='
rg -c '^\s*claim\b' /tmp/audit-work/candidate-src/spec.k

if rg -n '\[(functional|simplification|concrete|owise|priority|anywhere)' \
  /tmp/audit-work/candidate-src/semantic.k \
  /tmp/audit-work/candidate-src/verification.k \
  /tmp/audit-work/candidate-src/spec.k
then
  printf 'special_rule_attributes_present=yes\n'
else
  printf 'special_rule_attributes_present=no\n'
fi
