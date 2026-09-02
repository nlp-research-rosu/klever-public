#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/131-digits
proofdef="$scratch/verification-fresh-kompiled"
failures=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then failures=1; fi
  return 0
}

run_proof() {
  label=$1
  shift
  printf '\nGROUND PROOF TARGET: %s\n$' "$label"
  printf ' %q' timeout 300s kprove "$@"
  printf '\n'
  output=$(timeout 300s kprove "$@" 2>&1)
  status=$?
  printf '%s\n[exit %d]\n' "$output" "$status"
  if (( status != 0 )) || ! printf '%s\n' "$output" | grep -qx '#Top'; then
    printf 'ground_proof_check=FAIL target=%s\n' "$label"
    failures=1
  else
    printf 'ground_proof_check=PASS target=%s exit=0 output=#Top\n' "$label"
  fi
}

printf 'AUDIT STAGE 4: ADEQUACY, WITNESSES, AND PROGRAM PINNING\n'

run cp /audit-output/evidence/04_ground_witnesses.k \
  "$scratch/04_ground_witnesses.k"

# These ground claims contain no symbolic loop lemma, so each finite execution
# must reach the stated numerical result directly under the rebuilt semantics.
run_proof loop-235-direct "$scratch/04_ground_witnesses.k" \
  --definition "$proofdef" --spec-module GROUND-WITNESSES \
  --claims GROUND-WITNESSES.loop-235
run_proof entry-235-direct "$scratch/04_ground_witnesses.k" \
  --definition "$proofdef" --spec-module GROUND-WITNESSES \
  --claims GROUND-WITNESSES.entry-235

run python3 /audit-output/evidence/03_python_case.py 235

# Body-sensitivity test: change the generated program's decimal remainder
# operation from 10 to 11, regenerate with the trusted translator, and require
# the proof-side structural identity check to stop matching.
printf '\n$ sed %q %q > %q\n' \
  '0,/n % 10/s//n % 11/' "$scratch/solution.py" \
  "$scratch/solution.body-mutated.py"
sed '0,/n % 10/s//n % 11/' "$scratch/solution.py" \
  > "$scratch/solution.body-mutated.py"
status=$?
printf '[exit %d]\n' "$status"
if (( status != 0 )); then failures=1; fi

printf '\n$ python3 /reference/py2mpy.py %q > %q\n' \
  "$scratch/solution.body-mutated.py" "$scratch/solution.body-mutated.mpy"
python3 /reference/py2mpy.py "$scratch/solution.body-mutated.py" \
  > "$scratch/solution.body-mutated.mpy"
status=$?
printf '[exit %d]\n' "$status"
if (( status != 0 )); then failures=1; fi

mutated_check="$scratch/inputs/check_solution_program_mutated.mpy"
printf '\n$ sed %q %q > %q\n' \
  '1s/^/CheckProgram(SolutionProgram, /; $s/$/)/' \
  "$scratch/solution.body-mutated.mpy" "$mutated_check"
sed '1s/^/CheckProgram(SolutionProgram, /; $s/$/)/' \
  "$scratch/solution.body-mutated.mpy" > "$mutated_check"
status=$?
printf '[exit %d]\n' "$status"
if (( status != 0 )); then failures=1; fi

printf '\n$ krun %q --definition %q --output pretty\n' \
  "$mutated_check" "$proofdef"
mutated_output=$(krun "$mutated_check" --definition "$proofdef" --output pretty 2>&1)
status=$?
printf '%s\n[exit %d]\n' "$mutated_output" "$status"
compact=$(printf '%s' "$mutated_output" | tr -d '[:space:]')
if [[ "$compact" == *ProgramsMatch* ]]; then
  printf 'program_body_sensitivity=FAIL (mutation still matched)\n'
  failures=1
elif [[ "$compact" == *CheckProgram* ]]; then
  printf 'program_body_sensitivity=PASS (mutation left structural check stuck)\n'
else
  printf 'program_body_sensitivity=FAIL (unexpected negative-check behavior)\n'
  failures=1
fi

printf '\n$ python3 -c %q %q\n' \
  'import importlib.util,sys; p=importlib.util.spec_from_file_location("m",sys.argv[1]); m=importlib.util.module_from_spec(p); p.loader.exec_module(m); print(m.digits(235))' \
  "$scratch/solution.body-mutated.py"
python3 -c \
  'import importlib.util,sys; p=importlib.util.spec_from_file_location("m",sys.argv[1]); m=importlib.util.module_from_spec(p); p.loader.exec_module(m); print(m.digits(235))' \
  "$scratch/solution.body-mutated.py"
status=$?
printf '[exit %d]\n' "$status"
if (( status != 0 )); then failures=1; fi

printf '\nstage4_failures=%d\n' "$failures"
exit "$failures"
