#!/usr/bin/env bash
set -u

work=/tmp/audit-work/review-83
cd "$work" || exit 99
status=0

echo "tool versions"
echo "command: kompile --version"
kompile --version
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi
echo "command: kprove --version"
kprove --version
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "fresh-output precondition checks"
for path in fresh-semantic-kompiled fresh-verification-kompiled; do
  if test -e "$path" || test -L "$path"; then
    echo "BAD: pre-existing output path $work/$path"
    status=1
  else
    echo "OK absent: $work/$path"
  fi
done

echo "command: kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX --output-definition fresh-semantic-kompiled"
kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-semantic-kompiled
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

for n in 1 2 3 5 10; do
  echo "command: krun solution.mpy --definition fresh-semantic-kompiled -cN=$n"
  output=$(krun solution.mpy --definition fresh-semantic-kompiled -cN="$n" 2>&1)
  rc=$?
  printf '%s\n' "$output"
  echo "exit: $rc"
  expected=$(python3 -c 'import solution, sys; print(solution.starts_one_ends(int(sys.argv[1])))' "$n")
  py_rc=$?
  echo "python command: python3 -c import-solution-and-call $n"
  echo "python exit: $py_rc"
  echo "python expected: $expected"
  if (( rc != 0 || py_rc != 0 )); then
    status=1
  elif grep -Fq "result ( $expected )" <<<"$output"; then
    echo "K/Python comparison: MATCH"
  else
    echo "K/Python comparison: MISMATCH"
    status=1
  fi
done

echo "command: kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition fresh-verification-kompiled"
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

for claim in SPEC.positive-n-one SPEC.positive-n-gt-one; do
  echo "command: kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC --claims $claim"
  output=$(kprove spec.k \
    --definition fresh-verification-kompiled \
    --spec-module SPEC \
    --claims "$claim" 2>&1)
  rc=$?
  printf '%s\n' "$output"
  echo "exit: $rc"
  if (( rc == 0 )) && grep -Fxq '#Top' <<<"$output"; then
    echo "claim result: CLOSED (#Top and exit 0)"
  else
    echo "claim result: NOT CLOSED"
    status=1
  fi
done

echo "command: kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC"
output=$(kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC 2>&1)
rc=$?
printf '%s\n' "$output"
echo "exit: $rc"
if (( rc == 0 )) && grep -Fxq '#Top' <<<"$output"; then
  echo "combined result: CLOSED (#Top and exit 0)"
else
  echo "combined result: NOT CLOSED"
  status=1
fi

echo "script_exit: $status"
exit "$status"
