#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/131-digits
semdef="$scratch/semantic-fresh-kompiled"
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

run_case() {
  input=$1
  invoke="$scratch/inputs/digits_${input}.mpy"

  printf '\n$ sed %q %q > %q\n' \
    "1s/^/Invoke(/; \$s/\$/, \\\"digits\\\", ${input})/" \
    "$scratch/solution.regenerated.mpy" "$invoke"
  sed "1s/^/Invoke(/; \$s/\$/, \\\"digits\\\", ${input})/" \
    "$scratch/solution.regenerated.mpy" > "$invoke"
  status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then failures=1; return; fi

  printf '\n$ python3 /audit-output/evidence/03_python_case.py %q\n' "$input"
  oracle_output=$(python3 /audit-output/evidence/03_python_case.py "$input" 2>&1)
  status=$?
  printf '%s\n[exit %d]\n' "$oracle_output" "$status"
  if (( status != 0 )); then failures=1; return; fi
  expected=$(printf '%s\n' "$oracle_output" | sed -n 's/^expected=//p')

  printf '\n$ krun %q --definition %q --output pretty\n' "$invoke" "$semdef"
  k_output=$(krun "$invoke" --definition "$semdef" --output pretty 2>&1)
  status=$?
  printf '%s\n[exit %d]\n' "$k_output" "$status"
  if (( status != 0 )); then failures=1; return; fi

  compact=$(printf '%s' "$k_output" | tr -d '[:space:]')
  if [[ "$compact" == *"<answer>${expected}~>.K</answer>"* ]]; then
    printf 'comparison=PASS input=%s expected=%s\n' "$input" "$expected"
  else
    printf 'comparison=FAIL input=%s expected=%s\n' "$input" "$expected"
    failures=1
  fi
}

run_proof() {
  label=$1
  shift
  printf '\nPROOF TARGET: %s\n$' "$label"
  printf ' %q' timeout 300s kprove "$@"
  printf '\n'
  proof_output=$(timeout 300s kprove "$@" 2>&1)
  status=$?
  printf '%s\n[exit %d]\n' "$proof_output" "$status"
  if (( status != 0 )) || ! printf '%s\n' "$proof_output" | grep -qx '#Top'; then
    printf 'proof_check=FAIL target=%s\n' "$label"
    failures=1
  else
    printf 'proof_check=PASS target=%s exit=0 output=#Top\n' "$label"
  fi
}

printf 'AUDIT STAGE 3: CLEAN RECONSTRUCTION, EXECUTION, AND PROOF\n'
run kompile --version
run kprove --version

printf '\nCandidate compiled definitions deliberately excluded from scratch copy:\n'
run find "$scratch" -maxdepth 1 -type d -name '*-kompiled' -printf '%p\n'

run kompile "$scratch/semantic.k" \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition "$semdef"

run mkdir -p "$scratch/inputs"
run_case 0
run_case 1
run_case 4
run_case 10
run_case 11
run_case 22
run_case 235
run_case 2468
run_case 10203
run_case 13579
run_case 1111111111111111111111111111111111111111

run cp /audit-output/evidence/03_spec_labeled.k "$scratch/03_spec_labeled.k"

run kompile "$scratch/verification.k" \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  --output-definition "$proofdef"

program_check="$scratch/inputs/check_solution_program.mpy"
printf '\n$ sed %q %q > %q\n' \
  '1s/^/CheckProgram(SolutionProgram, /; $s/$/)/' \
  "$scratch/solution.regenerated.mpy" "$program_check"
sed '1s/^/CheckProgram(SolutionProgram, /; $s/$/)/' \
  "$scratch/solution.regenerated.mpy" > "$program_check"
status=$?
printf '[exit %d]\n' "$status"
if (( status != 0 )); then failures=1; fi

printf '\n$ krun %q --definition %q --output pretty\n' \
  "$program_check" "$proofdef"
check_output=$(krun "$program_check" --definition "$proofdef" --output pretty 2>&1)
status=$?
printf '%s\n[exit %d]\n' "$check_output" "$status"
compact_check=$(printf '%s' "$check_output" | tr -d '[:space:]')
if (( status == 0 )) && [[ "$compact_check" == *'<k>ProgramsMatch~>.K</k>'* ]]; then
  printf 'program_identity_check=PASS\n'
else
  printf 'program_identity_check=FAIL\n'
  failures=1
fi

run_proof all-claims "$scratch/03_spec_labeled.k" \
  --definition "$proofdef" --spec-module SPEC-LABELED
run_proof loop-invariant "$scratch/03_spec_labeled.k" \
  --definition "$proofdef" --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.loop-invariant
run_proof entry-contract "$scratch/03_spec_labeled.k" \
  --definition "$proofdef" --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.entry-contract

printf '\nstage3_failures=%d\n' "$failures"
exit "$failures"
