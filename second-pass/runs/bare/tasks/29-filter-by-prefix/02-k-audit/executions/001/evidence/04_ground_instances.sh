#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate || exit 90

printf '%s\n' 'COMMAND: kprove ground-instances.k --definition /tmp/audit-work/proof-kompiled --spec-module GROUND-INSTANCES --dry-run'
kprove ground-instances.k \
  --definition /tmp/audit-work/proof-kompiled \
  --spec-module GROUND-INSTANCES \
  --dry-run
status=$?
printf 'EXIT: %s\n\n' "$status"
if test "$status" -ne 0; then
  exit "$status"
fi

printf '%s\n' 'COMMAND: kprove ground-instances.k --definition /tmp/audit-work/proof-kompiled --spec-module GROUND-INSTANCES'
kprove ground-instances.k \
  --definition /tmp/audit-work/proof-kompiled \
  --spec-module GROUND-INSTANCES
status=$?
printf 'EXIT: %s\n\n' "$status"
if test "$status" -ne 0; then
  exit "$status"
fi

printf '%s\n' 'COMMAND: compare instantiated results with both Python implementations'
python3 - <<'PY'
import importlib.util
from pathlib import Path

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_prefix

canonical = load("ground_canonical", "/tmp/audit-work/trusted/canonical.py")
generated = load("ground_generated", "/tmp/audit-work/candidate/solution.py")
program_input = ["abc", "bcd", "cde", "array"]
program_expected = ["abc", "array"]
loop_remaining = ["abc", "b"]
loop_acc = ["prior"]
loop_expected = ["prior", "abc"]
print("program canonical:", canonical(program_input, "a"))
print("program generated:", generated(program_input, "a"))
print("program claimed:", program_expected)
print("loop ACC + canonical(remaining):", loop_acc + canonical(loop_remaining, "a"))
print("loop ACC + generated(remaining):", loop_acc + generated(loop_remaining, "a"))
print("loop claimed:", loop_expected)
assert canonical(program_input, "a") == generated(program_input, "a") == program_expected
assert loop_acc + canonical(loop_remaining, "a") == loop_expected
assert loop_acc + generated(loop_remaining, "a") == loop_expected
PY
status=$?
printf 'EXIT: %s\n' "$status"
exit "$status"
