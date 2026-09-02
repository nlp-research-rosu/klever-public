#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/111-histogram
definition="$scratch/semantic-audit-kompiled"
program="$scratch/solution.mpy"
overall=0

cases=(
  '""'
  '"a"'
  '"a b c"'
  '"a b b a"'
  '"b b b b a"'
  '"a  b"'
  '" a"'
)

for k_literal in "${cases[@]}"; do
  printf 'CASE_K_LITERAL: %s\n' "$k_literal"
  printf 'COMMAND: krun %q --definition %q -cTEST=%q --output pretty\n' \
    "$program" "$definition" "$k_literal"
  krun "$program" --definition "$definition" -cTEST="$k_literal" --output pretty
  status=$?
  printf 'KRUN_EXIT_STATUS: %d\n' "$status"
  if [[ $status -ne 0 ]]; then
    overall=$status
  fi
done

printf 'PYTHON_COMPARISON_RESULTS:\n'
python3 - <<'PY'
import importlib.util
import json
from pathlib import Path

path = Path("/tmp/audit-work/111-histogram/solution.py")
spec = importlib.util.spec_from_file_location("concrete_solution", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

cases = ["", "a", "a b c", "a b b a", "b b b b a", "a  b", " a"]
for text in cases:
    print(json.dumps({"input": text, "python_result": module.histogram(text)},
                     sort_keys=True))
PY
python_status=$?
printf 'PYTHON_EXIT_STATUS: %d\n' "$python_status"
if [[ $python_status -ne 0 ]]; then
  overall=$python_status
fi

exit "$overall"
