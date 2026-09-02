#!/usr/bin/env bash
set -u

definition=/tmp/audit-work/candidate-src/semantic-kompiled-clean
program=/tmp/audit-work/candidate-src/solution.mpy
cases=(-1 0 1 2 3 4 6 8 9 15 16 25 31 49 101 13441)
mismatches=0

for n in "${cases[@]}"; do
  python_json=$(
    env PYTHONDONTWRITEBYTECODE=1 \
      python3 /audit-output/evidence/python_case.py "$n"
  )
  python_status=$?
  if [[ $python_status -ne 0 ]]; then
    echo "PYTHON_DIVERGENCE n=$n status=$python_status output=$python_json"
    mismatches=$((mismatches + 1))
    continue
  fi

  if grep -q '"generated": true' <<<"$python_json"; then
    expected=true
  else
    expected=false
  fi

  k_output=$(krun "$program" --definition "$definition" -cN="$n" 2>&1)
  k_status=$?
  result_cell=$(
    sed -n '/<result>/,/<\/result>/p' <<<"$k_output" | tr -d '[:space:]'
  )

  echo "CASE n=$n expected=Bool($expected) k_status=$k_status k_result=$result_cell"
  if [[ $k_status -ne 0 || "$result_cell" != "<result>Bool($expected)</result>" ]]; then
    echo "K_OUTPUT_BEGIN"
    printf '%s\n' "$k_output"
    echo "K_OUTPUT_END"
    mismatches=$((mismatches + 1))
  fi
done

echo "CASE_COUNT=${#cases[@]}"
echo "MISMATCH_COUNT=$mismatches"
exit "$mismatches"
