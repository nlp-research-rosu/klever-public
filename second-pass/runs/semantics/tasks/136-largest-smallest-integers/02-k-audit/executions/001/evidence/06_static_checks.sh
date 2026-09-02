#!/usr/bin/env bash
set -u

status=0
scratch=/tmp/audit-work/reconstruction
kore="$scratch/bridge-audit-kompiled/definition.kore"

printf 'COMMAND: bash /audit-output/evidence/06_static_checks.sh\n'
printf 'STAGE: fixed-semantics generated sort predicate and proof projection equations\n'
printf 'RUN: extract bounded KORE rule comments for isInt and intValue\n'
rg -n --max-columns 500 --max-columns-preview \
  '^// rule (isInt\(|.*intValue)' "$kore" \
  | sed -n '1,40p'
kore_extract_status=${PIPESTATUS[0]}
printf 'EXIT KORE predicate extraction: %d\n' "$kore_extract_status"
if [[ "$kore_extract_status" -ne 0 ]]; then
  status=1
fi

printf 'STAGE: proof-definition exclusion of concrete-only rules\n'
concrete_count=$(rg -c 'Source\(.*/semantics/concrete\.k\)' \
  "$scratch/fresh-verification-kompiled/definition.kore" || true)
concrete_count=${concrete_count:-0}
printf 'concrete.k source rules in proof definition=%s expected=0\n' "$concrete_count"
if [[ "$concrete_count" -ne 0 ]]; then
  status=1
fi

printf 'STAGE: proof-local guard overlap, coverage, and source-equation checks\n'
printf 'RUN: python3 /audit-output/evidence/extension_equation_checks.py\n'
python3 /audit-output/evidence/extension_equation_checks.py
equation_status=$?
printf 'EXIT equation checks: %d\n' "$equation_status"
if [[ "$equation_status" -ne 0 ]]; then
  status=1
fi

printf 'STAGE: candidate proof-local special attributes\n'
printf 'RUN: rg attributes in verification.k\n'
rg -n '\[(function|total|functional|priority|simplification|no-evaluators|concrete)[^]]*\]' \
  "$scratch/verification.k"
attribute_status=$?
printf 'EXIT proof-local attribute inventory: %d\n' "$attribute_status"
if [[ "$attribute_status" -ne 0 ]]; then
  status=1
fi

printf 'FINAL EXIT: %d\n' "$status"
exit "$status"
