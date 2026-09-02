#!/usr/bin/env bash
set -u

work=/tmp/audit-work/review-83
status=0

echo "command: sed module rename and Int(18)->Int(19) in both literal program bodies"
sed \
  -e 's/ADEQUACY-GROUND/BODY-SENSITIVITY/g' \
  -e 's/Int(18)/Int(19)/g' \
  /audit-output/evidence/adequacy-ground.k \
  > /audit-output/evidence/body-sensitivity.k
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "command: diff -u adequacy-ground.k body-sensitivity.k (exit 1 means intended differences)"
diff -u \
  /audit-output/evidence/adequacy-ground.k \
  /audit-output/evidence/body-sensitivity.k
rc=$?
echo "exit: $rc"
if (( rc != 1 )); then status=1; fi

echo "command: cp body-sensitivity.k $work/body-sensitivity.k"
cp /audit-output/evidence/body-sensitivity.k "$work/body-sensitivity.k"
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

cd "$work" || exit 99
echo "command: kprove body-sensitivity.k --definition fresh-verification-kompiled --spec-module BODY-SENSITIVITY --claims BODY-SENSITIVITY.witness-n-two --dry-run"
kprove body-sensitivity.k \
  --definition fresh-verification-kompiled \
  --spec-module BODY-SENSITIVITY \
  --claims BODY-SENSITIVITY.witness-n-two \
  --dry-run
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "command: kprove body-sensitivity.k --definition fresh-verification-kompiled --spec-module BODY-SENSITIVITY --claims BODY-SENSITIVITY.witness-n-two"
output=$(kprove body-sensitivity.k \
  --definition fresh-verification-kompiled \
  --spec-module BODY-SENSITIVITY \
  --claims BODY-SENSITIVITY.witness-n-two 2>&1)
rc=$?
printf '%s\n' "$output"
echo "exit: $rc"
if (( rc != 0 )) && grep -Eq 'WarnStuckClaimState|implication check.*failed|cannot be rewritten further' <<<"$output"; then
  echo "body sensitivity result: EXPECTED RESULT-CONSTRAINT FAILURE"
else
  echo "body sensitivity result: BAD (mutation closed or failed for unrelated reason)"
  status=1
fi

echo "witness: n=2; mutated program returns 19, retained obligation requires 18"
echo "script_exit: $status"
exit "$status"
