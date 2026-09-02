#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/reconstruction

run_case() {
  local x_value="$1"
  local n_value="$2"
  local expected="$3"
  local args
  local output
  args="strVal(\"${x_value}\"),strVal(\"${n_value}\")"
  output="$(krun solution.mpy -cARGS="$args" \
    --definition audit-semantic-kompiled)"
  printf '%s\n' "$output"
  grep -Fq "result ( boolVal ( ${expected} ) )" <<<"$output"
  python3 - "$x_value" "$n_value" "$expected" <<'PY'
import sys
from solution import simplify

x, n, expected_text = sys.argv[1:]
actual = simplify(x, n)
expected = expected_text == "true"
print(f"python simplify({x!r}, {n!r})={actual}; expected={expected}")
raise SystemExit(0 if actual == expected else 1)
PY
}

run_case "1/5" "5/1" true
run_case "1/6" "2/1" false
run_case "1/1" "1/1" true
run_case "0001/0006" "0002/0001" false
run_case "18014398509481985/2" "1/1" false
run_case "10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000/1" "1/1" true
