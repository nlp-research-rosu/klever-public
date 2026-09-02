#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate || exit 90

for claim in ground-empty ground-ints; do
  printf '\n$ kprove spec-ground.k --definition audit-verification-kompiled --spec-module SUM-SQUARES-GROUND-SPEC --claims SUM-SQUARES-GROUND-SPEC.%s --output pretty\n' "$claim"
  output=$(kprove spec-ground.k \
    --definition audit-verification-kompiled \
    --spec-module SUM-SQUARES-GROUND-SPEC \
    --claims "SUM-SQUARES-GROUND-SPEC.$claim" \
    --output pretty 2>&1)
  status=$?
  printf '%s\n' "$output"
  printf 'EXIT: %s\n' "$status"
  if (( status != 0 )) || ! grep -Fxq '#Top' <<<"$output"; then
    exit 1
  fi
done

printf '\n%s\n' 'NOTE: the ground-float Haskell claim is intentionally not rerun here.'
printf '%s\n' 'The prior retry log records the backend missing FLOAT.ceil; LLVM concrete assertions cover the float witness.'

printf '\n%s\n' '$ python3 -c canonical/candidate ground values'
python3 - <<'PY'
import importlib.util

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

canonical = load("/reference/canonical.py", "ground_canonical")
candidate = load("/tmp/audit-work/candidate/solution.py", "ground_candidate")
for case in ([], [1, 2, 3], [1.4, 4.2, 0]):
    print(case, canonical.sum_squares(case), candidate.sum_squares(case))
PY
status=$?
printf 'EXIT: %s\n' "$status"
exit "$status"
