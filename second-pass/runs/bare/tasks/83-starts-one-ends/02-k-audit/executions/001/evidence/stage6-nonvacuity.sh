#!/usr/bin/env bash
set -u

work=/tmp/audit-work/review-83
status=0

echo "command: create fresh result-plus-one mutation from candidate spec"
sed \
  -e 's/module SPEC$/module SPEC-VACUITY/' \
  -e 's/result(qualifyingCount(1))/result(qualifyingCount(1) +Int 1)/' \
  -e 's/result(qualifyingCount(N))/result(qualifyingCount(N) +Int 1)/' \
  /candidate/spec.k \
  > /audit-output/evidence/spec-vacuity.k
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "command: diff -u /candidate/spec.k /audit-output/evidence/spec-vacuity.k (exit 1 means intended differences)"
diff -u /candidate/spec.k /audit-output/evidence/spec-vacuity.k
rc=$?
echo "exit: $rc"
if (( rc != 1 )); then status=1; fi

echo "command: cp spec-vacuity.k $work/spec-vacuity.k"
cp /audit-output/evidence/spec-vacuity.k "$work/spec-vacuity.k"
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

cd "$work" || exit 99
echo "command: kprove spec-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-VACUITY --claims SPEC-VACUITY.positive-n-gt-one --dry-run"
kprove spec-vacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.positive-n-gt-one \
  --dry-run
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "satisfying witness: N=2 because 2 > 1"
actual=$(python3 -c 'import solution; print(solution.starts_one_ends(2))')
rc=$?
echo "command: python3 generated solution at N=2"
echo "exit: $rc"
echo "actual result: $actual"
mutated=$((actual + 1))
echo "mutated obligation: $mutated"
if (( rc != 0 || actual != 18 || mutated != 19 )); then status=1; fi

echo "command: kprove spec-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-VACUITY --claims SPEC-VACUITY.positive-n-gt-one"
output=$(kprove spec-vacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.positive-n-gt-one 2>&1)
rc=$?
printf '%s\n' "$output"
echo "exit: $rc"
if (( rc != 0 )) && grep -Eq 'WarnStuckClaimState|implication check.*failed|cannot be rewritten further' <<<"$output"; then
  echo "non-vacuity result: EXPECTED UNMET RESULT OBLIGATION"
else
  echo "non-vacuity result: BAD (mutation closed or failed for unrelated reason)"
  status=1
fi

echo "script_exit: $status"
exit "$status"
