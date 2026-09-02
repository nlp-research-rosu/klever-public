#!/usr/bin/env bash
set -u

definition=/tmp/audit-work/build/semantic-llvm-kompiled
program=/tmp/audit-work/source/solution.mpy
solution=/tmp/audit-work/source/solution.py
status=0
cases=(
  '3 5'
  '25 15'
  '0 0'
  '0 7'
  '7 0'
  '1 1'
  '-1 0'
  '0 -1'
  '-25 15'
  '25 -15'
  '-25 -15'
  '1071 462'
  '9223372036854775807 2147483647'
)

printf 'definition=%s\n' "$definition"
printf 'program=%s\n' "$program"
printf 'case_count=%d\n' "${#cases[@]}"
for pair in "${cases[@]}"; do
  read -r a b <<<"$pair"
  krun_output=$(krun "$program" --definition "$definition" -cA="$a" -cB="$b")
  krun_status=$?
  k_result=$(
    sed -n 's/.*result ( \(-\{0,1\}[0-9][0-9]*\) ).*/\1/p' <<<"$krun_output" |
      head -n 1
  )
  python_result=$(
    python3 - "$solution" "$a" "$b" <<'PY'
import importlib.util
import sys

path, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
spec = importlib.util.spec_from_file_location("semantic_oracle_solution", path)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)
print(module.greatest_common_divisor(a, b))
PY
  )
  math_result=$(
    python3 - "$a" "$b" <<'PY'
import math
import sys
print(math.gcd(int(sys.argv[1]), int(sys.argv[2])))
PY
  )
  printf 'A=%s B=%s krun_exit=%d K=%s generated_python=%s math.gcd=%s\n' \
    "$a" "$b" "$krun_status" "$k_result" "$python_result" "$math_result"
  if (( krun_status != 0 )) ||
     [[ -z "$k_result" || "$k_result" != "$python_result" || "$k_result" != "$math_result" ]]; then
    status=1
  fi
done

printf 'MISMATCH_FREE=%s\n' "$([[ "$status" -eq 0 ]] && printf YES || printf NO)"
exit "$status"
