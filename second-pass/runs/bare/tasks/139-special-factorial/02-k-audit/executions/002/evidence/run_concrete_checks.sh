#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/candidate-src
definition="$work/audit-concrete-kompiled"

for n in 1 2 4 6; do
  echo "COMMAND: krun solution.mpy -cN=$n --definition $definition --output pretty"
  output="$(cd "$work" && krun solution.mpy -cN="$n" \
    --definition "$definition" --output pretty)"
  status=$?
  echo "$output"
  echo "EXIT: $status"
  expected="$(python3 - "$n" <<'PY'
import importlib.util
import sys

path = "/tmp/audit-work/trusted/canonical.py"
spec = importlib.util.spec_from_file_location("trusted_canonical_139_concrete", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(module.special_factorial(int(sys.argv[1])))
PY
)"
  candidate="$(python3 - "$n" <<'PY'
import importlib.util
import sys

path = "/tmp/audit-work/candidate-src/solution.py"
spec = importlib.util.spec_from_file_location("candidate_139_concrete", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(module.special_factorial(int(sys.argv[1])))
PY
)"
  echo "ORACLES: n=$n canonical=$expected candidate=$candidate"
  grep -Fq "result ( $expected )" <<<"$output"
  test "$candidate" = "$expected"
  echo "COMPARE: PASS n=$n"
done
