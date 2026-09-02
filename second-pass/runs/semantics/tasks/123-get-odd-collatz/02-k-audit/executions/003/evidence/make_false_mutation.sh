#!/usr/bin/env bash
set -euo pipefail

scratch_root=/tmp/audit-work/fresh
evidence_root=/audit-output/evidence
source_spec="$scratch_root/spec.k"
mutant_spec="$scratch_root/spec-vacuity-audit.k"

correct_result='1 |-> list(sortVS(vCons(5, vCons(1, .ValSeq))))'
false_result='1 |-> list(sortVS(vCons(5, vCons(3, vCons(1, .ValSeq)))))'

source_count=$(grep -F -c "$correct_result" "$source_spec")
if [[ "$source_count" -ne 1 ]]; then
  echo "expected exactly one case-5 result line, observed $source_count" >&2
  exit 1
fi

sed \
  -e 's/module SPEC$/module SPEC-VACUITY-AUDIT/' \
  -e "s/$correct_result/$false_result/" \
  "$source_spec" \
  > "$mutant_spec"

false_count=$(grep -F -c "$false_result" "$mutant_spec")
if [[ "$false_count" -ne 1 ]]; then
  echo "expected exactly one false result line, observed $false_count" >&2
  exit 1
fi

cp -a "$mutant_spec" "$evidence_root/spec-vacuity-audit.k"
{
  diff -u "$source_spec" "$mutant_spec" || [[ $? -eq 1 ]]
} > "$evidence_root/spec-vacuity-audit.diff"

printf 'SATISFYING_WITNESS=n=5; candidate and canonical both return [1, 5]\n'
printf 'FALSE_OBLIGATION=returned heap list contains an additional 3: [1, 3, 5]\n'
printf 'MUTATION_COUNT=%s\n' "$false_count"
