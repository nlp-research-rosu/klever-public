#!/usr/bin/env bash
set -euo pipefail
trap 'rc=$?; echo "EXIT_STATUS=$rc"' EXIT

definition=/tmp/audit-work/11-string-xor/build/semantic-kompiled
program=/tmp/audit-work/11-string-xor/source/solution.mpy
k_output=/tmp/audit-work/11-string-xor/recursion-boundary-k.out

echo 'COMMAND: bash /audit-output/evidence/02_recursion_boundary.sh'
echo 'COMMAND: python3 /audit-output/evidence/02_recursion_boundary.py'
python3 /audit-output/evidence/02_recursion_boundary.py

echo 'COMMAND: krun solution.mpy at segment length 998 under generated semantics'
krun "$program" \
  --definition "$definition" \
  -cARGS='Args(str(segment(998,seed(0))),str(segment(998,seed(0))))' \
  --output pretty \
  > "$k_output"
k_status=$?
echo "K_LONG_INPUT_EXIT_STATUS=$k_status"
wc -lc "$k_output"
head -n 5 "$k_output"
tail -n 5 "$k_output"
false_cons_count=$(grep -oF 'cons ( false' "$k_output" | wc -l)
echo "K_RETURNED_FALSE_BITS=$false_cons_count"
test "$false_cons_count" -eq 998
grep -F 'returned ( str (' "$k_output" > /dev/null
echo 'K_SEMANTICS_NORMAL_RETURN_AT_LENGTH_998=true'
