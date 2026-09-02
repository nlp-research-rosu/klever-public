#!/usr/bin/env bash
set -euo pipefail

work=$(mktemp -d /tmp/audit-work/k-operational.XXXXXX)
echo "work=$work"
cp /reference/k-proof/semantic.k /reference/k-proof/solution.mpy "$work"/
cd "$work"

echo "COMMAND kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX --output-definition semantic-kompiled"
kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled
echo "exit_code=$?"

run_case() {
  local input=$1
  local expected=$2
  local output

  echo "COMMAND krun solution.mpy --definition semantic-kompiled -cINPUT='$input' --output pretty"
  output=$(
    krun solution.mpy \
      --definition semantic-kompiled \
      -cINPUT="$input" \
      --output pretty
  )
  echo "$output"
  echo "exit_code=$?"
  if ! tr -d '[:space:]' <<<"$output" |
      grep -Fq "<result>intVal($expected)</result>"; then
    echo "EXPECTED result intVal($expected), but it was not observed" >&2
    return 1
  fi
}

run_case '""' 0
run_case '"2357BD"' 6
run_case '"2222"' 4
run_case '"ABED1A33"' 4
run_case '"b2DXYZ3"' 3
run_case '"22BBDDX"' 6

echo "all_operational_cases_passed=true"
