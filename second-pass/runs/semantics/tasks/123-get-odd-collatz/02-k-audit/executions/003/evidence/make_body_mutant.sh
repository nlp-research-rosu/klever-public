#!/usr/bin/env bash
set -euo pipefail

scratch_root=/tmp/audit-work/fresh
evidence_root=/audit-output/evidence/body-mutant
mkdir -p "$evidence_root"

sed \
  -e 's/module VERIFICATION$/module VERIFICATION-BODY-MUTANT/' \
  -e 's/Expr(Call(Attribute(Name("odd_numbers"), "append"), Name("n")))/Expr(Call(Attribute(Name("odd_numbers"), "append"), Int(1)))/g' \
  "$scratch_root/verification.k" \
  > "$scratch_root/verification-body-mutant.k"

sed \
  -e 's/requires "verification.k"/requires "verification-body-mutant.k"/' \
  -e 's/module SPEC$/module SPEC-BODY-MUTANT/' \
  -e 's/imports VERIFICATION$/imports VERIFICATION-BODY-MUTANT/' \
  "$scratch_root/spec.k" \
  > "$scratch_root/spec-body-mutant.k"

mutation_count=$(
  {
    diff -u "$scratch_root/verification.k" "$scratch_root/verification-body-mutant.k" \
      || [[ $? -eq 1 ]]
  } | grep -c '^+.*append"), Int(1)'
)
if [[ "$mutation_count" -ne 2 ]]; then
  echo "expected two executed-body mutations, observed $mutation_count" >&2
  exit 1
fi

cp -a \
  "$scratch_root/verification-body-mutant.k" \
  "$scratch_root/spec-body-mutant.k" \
  "$evidence_root/"

diff -u \
  "$scratch_root/verification.k" \
  "$scratch_root/verification-body-mutant.k" \
  > "$evidence_root/verification-body-mutant.diff" \
  || [[ $? -eq 1 ]]

printf 'MUTATION_COUNT=%s\n' "$mutation_count"
printf '%s\n' 'MUTATION=both embedded program bodies append Int(1) instead of Name("n") on the odd branch'
