#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT_STATUS=%s\n" "$status"' EXIT

SCRATCH=/tmp/audit-work/108-count-nums
cd "$SCRATCH"

set -x
python3 - <<'PY'
import sys

from canonical import count_nums as canonical
from solution import count_nums as candidate

print("CPYTHON_RECURSION_LIMIT", sys.getrecursionlimit())
tests = [
    ("long_list_1200", [1] * 1200),
    ("long_integer_1200_digits", [10**1199]),
]
for name, values in tests:
    print(name, "canonical", canonical(values))
    try:
        print(name, "candidate", candidate(values))
    except Exception as error:
        print(name, "candidate_raised", type(error).__name__)
PY
set +x

list_arg=VNil
for ((index=0; index<1200; index++)); do
  list_arg="VCons(1,$list_arg)"
done
printf "CONSTRUCTED_LIST_LENGTH=1200 ARG_BYTES=%s\n" "${#list_arg}"

set -x
timeout --signal=TERM --kill-after=10 120 \
  krun solution.mpy \
    --definition semantic-kompiled \
    -cARG="ListV($list_arg)" \
  | grep -F 'IntV ( 1200 ) ~> .K'
list_statuses=("${PIPESTATUS[@]}")
set +x
printf "K_LONG_LIST_PIPE_STATUSES=%s,%s\n" \
  "${list_statuses[0]}" "${list_statuses[1]}"
test "${list_statuses[0]}" -eq 0
test "${list_statuses[1]}" -eq 0

huge_integer=1
for ((index=0; index<1199; index++)); do
  huge_integer="${huge_integer}0"
done
printf "CONSTRUCTED_INTEGER_DIGITS=%s\n" "${#huge_integer}"

set -x
timeout --signal=TERM --kill-after=10 120 \
  krun solution.mpy \
    --definition semantic-kompiled \
    -cARG="list($huge_integer)" \
  | grep -F 'IntV ( 1 ) ~> .K'
integer_statuses=("${PIPESTATUS[@]}")
set +x
printf "K_LONG_INTEGER_PIPE_STATUSES=%s,%s\n" \
  "${integer_statuses[0]}" "${integer_statuses[1]}"
test "${integer_statuses[0]}" -eq 0
test "${integer_statuses[1]}" -eq 0
