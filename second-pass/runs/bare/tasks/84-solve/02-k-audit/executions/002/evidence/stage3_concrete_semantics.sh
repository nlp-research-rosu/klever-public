#!/usr/bin/env bash
set -uo pipefail
export PATH="/root/.nix-profile/bin:$PATH"

work=/tmp/audit-work/84-solve
definition="$work/concrete-kompiled"
status=0
inputs=(0 1 9 10 99 100 147 150 999 1000 9999 10000)

for value in "${inputs[@]}"; do
  expected=$(
    PYTHONPATH=/reference python3 -c \
      'import sys; from canonical import solve; print(solve(int(sys.argv[1])))' \
      "$value"
  )
  python_exit=$?
  output=$(krun "$work/solution.mpy" --definition "$definition" -cN="$value" 2>&1)
  krun_exit=$?
  printf 'INPUT %s EXPECTED %s PYTHON_EXIT %d KRUN_EXIT %d\n' \
    "$value" "$expected" "$python_exit" "$krun_exit"
  printf '%s\n' "$output"
  if [[ "$python_exit" -ne 0 || "$krun_exit" -ne 0 ]]; then
    status=1
    continue
  fi
  if grep -Fq "VStr ( \"$expected\" ) ~> .K" <<<"$output"; then
    printf 'MATCH %s\n' "$value"
  else
    printf 'MISMATCH %s\n' "$value"
    status=1
  fi
done

printf 'INPUT_COUNT %d\n' "${#inputs[@]}"
printf 'OVERALL_EXIT %d\n' "$status"
exit "$status"
