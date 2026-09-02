#!/usr/bin/env bash
set -u
set -o pipefail

work=/tmp/audit-work/submitted
definition="$work/verification-kompiled"

run() {
  echo "CMD: $*"
  "$@"
  local status=$?
  echo "EXIT: $status"
  return "$status"
}

echo 'CMD: kast submitted solution.mpy as Module with fresh verification definition, output KORE'
kast "$work/solution.mpy" \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  > "$work/04_submitted_module.kore"
status=$?
echo "EXIT: $status"
[[ $status -eq 0 ]] || exit "$status"

echo 'CMD: kast reviewer term solutionModule as Module with fresh verification definition, output KORE'
kast /audit-output/evidence/04_solution_module.term \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  > "$work/04_macro_module.kore"
status=$?
echo "EXIT: $status"
[[ $status -eq 0 ]] || exit "$status"

echo 'CMD: cmp -s parsed-submitted-module.kore parsed-solutionModule-macro.kore'
cmp -s "$work/04_submitted_module.kore" "$work/04_macro_module.kore"
status=$?
echo "EXIT: $status"
if [[ $status -ne 0 ]]; then
  diff -u "$work/04_submitted_module.kore" "$work/04_macro_module.kore"
  exit "$status"
fi

run cp /audit-output/evidence/04_ground_spec.k "$work/04_ground_spec.k" || exit $?

run kprove "$work/04_ground_spec.k" \
  --definition "$definition" \
  --spec-module SPEC-GROUND \
  --smt-timeout 10000 || exit $?

echo 'CMD: Python canonical and candidate evaluations at satisfying witness (3, 7)'
python3 - "$work" <<'PY'
import importlib.util
import pathlib
import sys

work = pathlib.Path(sys.argv[1])

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate_integers

canonical = load(work / "canonical.py", "canonical_ground")
candidate = load(work / "solution.py", "candidate_ground")
print("input=(3, 7)")
print("precondition=(3 > 0 and 7 > 0)=true")
print(f"canonical={canonical(3, 7)}")
print(f"candidate={candidate(3, 7)}")
print("claimed_evenDigits=[4, 6]")
if canonical(3, 7) != [4, 6] or candidate(3, 7) != [4, 6]:
    raise SystemExit(1)
PY
status=$?
echo "EXIT: $status"
exit "$status"
