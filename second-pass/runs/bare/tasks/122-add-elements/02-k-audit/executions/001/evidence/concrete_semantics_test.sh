#!/usr/bin/env bash
set -euo pipefail
set -x

export PATH=/home/agent/.nix-profile/bin:$PATH
audit_work=/tmp/audit-work/122-add-elements
cd "$audit_work"

run_case() {
  local name=$1
  local k_list=$2
  local n=$3
  local expected=$4
  local json_array=$5

  echo "CASE=$name EXPECTED=$expected"
  local k_output
  k_output=$(krun solution.mpy \
    --definition semantic-llvm-kompiled \
    -cARR="$k_list" \
    -cN="$n")
  echo "$k_output"
  grep -F "result ( $expected )" <<<"$k_output"
  python3 -c '
import json
import sys
from solution import add_elements
arr = json.loads(sys.argv[1])
k = int(sys.argv[2])
expected = int(sys.argv[3])
actual = add_elements(arr, k)
print(f"PYTHON_RESULT={actual}")
raise SystemExit(actual != expected)
' "$json_array" "$n" "$expected"
}

run_case \
  documented-example \
  'ListItem(111) ListItem(21) ListItem(3) ListItem(4000) ListItem(5) ListItem(6) ListItem(7) ListItem(8) ListItem(9)' \
  4 24 \
  '[111,21,3,4000,5,6,7,8,9]'

run_case \
  zero-iteration \
  'ListItem(7)' \
  0 0 \
  '[7]'

run_case \
  all-predicate-boundaries \
  'ListItem(-101) ListItem(-100) ListItem(-99) ListItem(-10) ListItem(-9) ListItem(-1) ListItem(0) ListItem(9) ListItem(10) ListItem(99) ListItem(100) ListItem(101)' \
  12 -1 \
  '[-101,-100,-99,-10,-9,-1,0,9,10,99,100,101]'

run_case \
  prefix-boundary \
  'ListItem(21) ListItem(-10) ListItem(4000) ListItem(3)' \
  1 21 \
  '[21,-10,4000,3]'
