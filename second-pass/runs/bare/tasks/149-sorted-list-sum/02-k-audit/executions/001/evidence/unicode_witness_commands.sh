#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT=%s\n" "$status"' EXIT
set -x

audit_work=/tmp/audit-work/audit149
overall=0
cd "$audit_work"

python3 /audit-output/evidence/generate_concrete_cases.py "$audit_work"

for case_name in emoji_single latin1_single combining_pair unicode_length_order unicode; do
  krun "audit-${case_name}.run" --definition semantic-kompiled \
    > "audit-${case_name}.focused.krun.out" 2>&1
  status=$?
  printf 'KRUN_EXIT case=%s status=%s\n' "$case_name" "$status"
  sed -n '1,80p' "audit-${case_name}.focused.krun.out"
  printf 'PYTHON_EXPECTED case=%s expected=%s\n' \
    "$case_name" "$(cat "audit-${case_name}.expected")"
  if (( status != 0 )); then
    overall=1
  elif grep -Fq -f "audit-${case_name}.expected" \
      "audit-${case_name}.focused.krun.out"; then
    printf 'KRUN_PYTHON_MATCH case=%s\n' "$case_name"
  else
    printf 'KRUN_PYTHON_DIVERGENCE case=%s\n' "$case_name"
    overall=1
  fi
done

printf 'UNICODE_WITNESS_OVERALL=%s\n' "$overall"
exit "$overall"
