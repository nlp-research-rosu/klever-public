#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/review-31
overall=0

printf 'COMMAND: factor 1000003\n'
factor 1000003
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then overall=1; fi

printf 'COMMAND: PYTHONDONTWRITEBYTECODE=1 python3 - [recursion witness]\n'
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import importlib.util
import sys

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_prime

def show(label, fn):
    try:
        print(label, ("return", fn(1_000_003)))
    except BaseException as error:
        print(label, ("raise", type(error).__name__, str(error)))

print("sys.getrecursionlimit()", sys.getrecursionlimit())
show(
    "trusted canonical",
    load("canonical", "/tmp/audit-work/review-31/reference/canonical.py"),
)
show(
    "submitted solution",
    load("submitted", "/tmp/audit-work/review-31/candidate/solution.py"),
)
PY
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then overall=1; fi

printf 'COMMAND: krun solution.mpy --definition %q -cN=1000003\n' \
  "$scratch/semantic-concrete-kompiled"
(
  cd "$scratch/candidate" &&
  krun solution.mpy \
    --definition "$scratch/semantic-concrete-kompiled" \
    -cN=1000003
) | sed -n '/<result>/,/<\/result>/p'
rc=${PIPESTATUS[0]}
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then overall=1; fi

printf 'STAGE5_WITNESS_OVERALL=%d\n' "$overall"
exit "$overall"
