#!/usr/bin/env bash
set -uo pipefail

run_krun() {
  local program=$1
  local input=$2
  local definition=$3
  printf '\n$ krun %q -cN=%q --definition %q\n' "$program" "$input" "$definition"
  krun "$program" -cN="$input" --definition "$definition"
  local status=$?
  printf '[exit %d]\n' "$status"
}

scratch=/tmp/audit-work/77-iscube
src="$scratch/candidate-src"
semdef="$scratch/audit-semantic-kompiled"
cubedef="$scratch/audit-cube-verification-kompiled"

printf '%s\n' 'Satisfying symbolic witnesses:'
printf '%s\n' 'cube-loop: N=2, I=1 gives a=8, n=1 and 0<=1<=2.'
printf '%s\n' 'nonnegative-cube: N=2 gives input 8 and 0<=2.'
printf '%s\n' 'negative-cube: N=2 gives input -8 and 0<2.'
printf '%s\n' 'gap-loop: N=2, D=1, I=1 gives a=9, n=1; 0<=1<=3 and 0<1<27-8.'
printf '%s\n' 'positive-noncube: N=2, D=1 gives input 9 and 0<1<27-8.'
printf '%s\n' 'negative-noncube: N=2, D=1 gives input -9 and the same gap conditions.'

printf '\n%s\n' 'Concrete submitted-program executions for entry witnesses:'
for input in 8 -8 9 -9; do
  run_krun "$src/solution.mpy" "$input" "$semdef"
done

printf '\n%s\n' 'Concrete iscubeProgram-abbreviation executions in the proof definition:'
for input in 8 -8 9 -9; do
  run_krun "$scratch/iscubeProgram.pgm" "$input" "$cubedef"
done

printf '\n$ python3 -c <compare trusted canonical and copied candidate on 8,-8,9,-9>\n'
python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.iscube

canonical = load("canonical", "/reference/canonical.py")
candidate = load("candidate", "/tmp/audit-work/77-iscube/candidate-src/solution.py")
for value in (8, -8, 9, -9):
    print(f"input={value} canonical={canonical(value)} candidate={candidate(value)}")
PY
printf '[exit %d]\n' "$?"
