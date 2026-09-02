#!/usr/bin/env bash
set -u

FRESH=/tmp/audit-work/fresh
overall=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
}

run_expect_failure() {
  local output
  output="$(mktemp /tmp/audit-work/expected-failure.XXXXXX.log)"
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$output" 2>&1
  local status=$?
  sed -n '1,240p' "$output"
  printf '[exit %d]\n' "$status"
  if (( status == 0 )); then
    printf '[UNEXPECTED] proof succeeded\n'
    overall=1
  elif rg -q 'WarnStuckClaimState|implication check between the conditions has failed' "$output"; then
    printf '[EXPECTED] proof failed with an unmet reachability obligation\n'
  else
    printf '[UNEXPECTED] non-zero result lacked a stuck-claim obligation\n'
    overall=1
  fi
  rm -f "$output"
}

printf '\n$ python3 /reference/py2mpy.py /audit-output/evidence/05_body-mutated-solution.py > /tmp/audit-work/fresh/05_body-mutated-solution.mpy\n'
python3 /reference/py2mpy.py \
  /audit-output/evidence/05_body-mutated-solution.py \
  > "$FRESH/05_body-mutated-solution.mpy"
translate_status=$?
printf '[exit %d]\n' "$translate_status"
if (( translate_status != 0 )); then
  overall=1
fi

run krun "$FRESH/05_body-mutated-solution.mpy" \
  --definition "$FRESH/concrete-kompiled" \
  -cN=1 \
  -cP=5

run python3 -c \
  'import importlib.util; p="/audit-output/evidence/05_body-mutated-solution.py"; s=importlib.util.spec_from_file_location("body_mutation",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print("mutated_python_result=",m.modp(1,5)); print("original_expected_result=",pow(2,1,5))'

run kprove /audit-output/evidence/05_body-mutation.k \
  -I "$FRESH" \
  --definition "$FRESH/proof-kompiled" \
  --spec-module AUDIT-BODY-MUTATION \
  --dry-run

run_expect_failure kprove /audit-output/evidence/05_body-mutation.k \
  -I "$FRESH" \
  --definition "$FRESH/proof-kompiled" \
  --spec-module AUDIT-BODY-MUTATION

run python3 -c \
  'print("vacuity_witness=(N=3,P=5)"); print("actual=",pow(2,3,5)); print("mutated_required=",pow(2,3,5)+1)'

run kprove /audit-output/evidence/06_spec-vacuity.k \
  -I "$FRESH" \
  --definition "$FRESH/proof-kompiled" \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run

run_expect_failure kprove /audit-output/evidence/06_spec-vacuity.k \
  -I "$FRESH" \
  --definition "$FRESH/proof-kompiled" \
  --spec-module AUDIT-SPEC-VACUITY

printf '\nOVERALL_EXIT=%d\n' "$overall"
exit "$overall"
