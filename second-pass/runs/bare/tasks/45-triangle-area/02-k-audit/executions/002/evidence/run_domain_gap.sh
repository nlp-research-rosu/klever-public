#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate || exit 1

printf '%s\n' '$ python3 -c <ordinary-float witness>'
python3 -c \
  'import importlib.util
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
c = load("c", "/tmp/audit-work/canonical.py")
s = load("s", "/tmp/audit-work/candidate/solution.py")
print("canonical triangle_area(0.5, 0.25) =", c.triangle_area(0.5, 0.25))
print("candidate triangle_area(0.5, 0.25) =", s.triangle_area(0.5, 0.25))'
python_status=$?
printf '[exit %d]\n' "$python_status"
if (( python_status != 0 )); then
  exit "$python_status"
fi

printf '%s\n' "$ krun solution.mpy --definition concrete-kompiled '-cARGS=Args(0.5, 0.25)'"
k_output="$(
  krun solution.mpy \
    --definition concrete-kompiled \
    '-cARGS=Args(0.5, 0.25)' 2>&1
)"
k_status=$?
printf '%s\n' "$k_output"
printf '[exit %d]\n' "$k_status"
if (( k_status == 0 )); then
  printf '%s\n' 'ERROR: generated integer-only argument syntax unexpectedly accepted floats'
  exit 1
fi
if [[ "$k_output" != *'Unexpected token'* && "$k_output" != *'parse'* ]]; then
  printf '%s\n' 'ERROR: float rejection was not a parser/domain rejection'
  exit 1
fi
printf '%s\n' 'EXPECTED DOMAIN GAP: ordinary Python float inputs are outside Args(Int,Int)'
