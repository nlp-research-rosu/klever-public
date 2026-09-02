#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/121-solution-audit
mutation="$scratch/body-mutation"
status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

run mkdir -p "$mutation"
run cp "$scratch/candidate/semantic.k" "$mutation/semantic.k"
run cp /audit-output/evidence/verification-body-mutation.k \
  "$mutation/verification-body-mutation.k"
run cp /audit-output/evidence/spec-body-mutation.k \
  "$mutation/spec-body-mutation.k"

printf '$ python3 %q %q > %q\n' \
  "$scratch/reference/py2mpy.py" \
  /audit-output/evidence/solution_operational_mutation.py \
  "$scratch/solution-operational-mutation.mpy"
python3 "$scratch/reference/py2mpy.py" \
  /audit-output/evidence/solution_operational_mutation.py \
  > "$scratch/solution-operational-mutation.mpy"
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then
  status=1
fi

run python3 /audit-output/evidence/body_mutation_check.py
run kompile "$mutation/verification-body-mutation.k" \
  --main-module VERIFICATION-BODY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition "$mutation/verification-body-mutation-kompiled"

printf '$ kprove %q --definition %q --spec-module SPEC-BODY-MUTATION --smt-timeout 1000\n' \
  "$mutation/spec-body-mutation.k" \
  "$mutation/verification-body-mutation-kompiled"
kprove "$mutation/spec-body-mutation.k" \
  --definition "$mutation/verification-body-mutation-kompiled" \
  --spec-module SPEC-BODY-MUTATION \
  --smt-timeout 1000
rc=$?
printf '[exit %d; expected nonzero for the changed executed body]\n' "$rc"
if [ "$rc" -eq 0 ]; then
  status=1
fi

exit "$status"
