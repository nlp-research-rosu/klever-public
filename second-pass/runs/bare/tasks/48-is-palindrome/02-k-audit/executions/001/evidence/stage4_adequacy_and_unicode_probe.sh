#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/48-is-palindrome
probe_dir="$scratch/probes"
definition="$scratch/build-final/semantic-llvm-kompiled"

printf '$ python3 %q %q > %q\n' \
  "$scratch/trusted/py2mpy.py" \
  "$probe_dir/reverse_solution.py" \
  "$probe_dir/reverse_solution.mpy"
python3 "$scratch/trusted/py2mpy.py" "$probe_dir/reverse_solution.py" \
  > "$probe_dir/reverse_solution.mpy" 2> "$probe_dir/reverse_translate.stderr"
status=$?
sed -n '1,120p' "$probe_dir/reverse_translate.stderr"
printf '[exit %d]\n' "$status"
test "$status" -eq 0 || exit "$status"

run sed -n 1,160p "$probe_dir/reverse_solution.mpy" || exit $?

for arg in '"aba"' '"ab"' '"éaé"' '"🙂a🙂"' '"áa"'
do
  run krun "$probe_dir/reverse_solution.mpy" \
    --definition "$definition" \
    '-cFUNCTION="reverse_only"' \
    "-cARG=$arg" \
    || exit $?
done

run python3 -c \
  'cases=["aba","ab","éaé","🙂a🙂","áa"]; print([(s, s[::-1]) for s in cases])' \
  || exit $?

run diff -u "$scratch/source/solution.mpy" "$scratch/regenerated-solution.mpy" \
  || exit $?
run rg -n \
  'Module|FuncDef|#invoke|isPalindrome|reverseString' \
  "$scratch/source/solution.mpy" \
  "$scratch/source/spec.k" \
  "$scratch/source/verification.k" \
  "$scratch/source/semantic.k" \
  || exit $?
