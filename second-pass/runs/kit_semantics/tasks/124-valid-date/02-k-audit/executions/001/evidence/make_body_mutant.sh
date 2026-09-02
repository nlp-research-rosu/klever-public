#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/fresh
source_verification=$scratch/verification.k
mutant_verification=$scratch/verification-body-mutant.k
mutant_spec=$scratch/spec-body-mutant.k

if ! sed -n '137p' "$source_verification" | grep -Fq 'Int(29)'; then
  printf 'expected February bound not found at verification.k:137\n' >&2
  exit 1
fi

sed '137s/Int(29)/Int(28)/' "$source_verification" > "$mutant_verification"
sed \
  -e '1s/verification.k/verification-body-mutant.k/' \
  -e 's/^module SPEC$/module SPEC-BODY-MUTANT/' \
  "$scratch/spec.k" > "$mutant_spec"

if cmp -s "$source_verification" "$mutant_verification"; then
  printf 'body mutant is unexpectedly identical to original\n' >&2
  exit 1
fi

printf 'mutated_source_line='
sed -n '137p' "$mutant_verification"
printf 'mutant_spec_header:\n'
sed -n '1,5p' "$mutant_spec"
printf 'changed_lines:\n'
diff -u "$source_verification" "$mutant_verification" || true
