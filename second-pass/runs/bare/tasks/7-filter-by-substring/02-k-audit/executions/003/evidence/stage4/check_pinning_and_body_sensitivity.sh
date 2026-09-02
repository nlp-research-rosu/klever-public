#!/usr/bin/env bash
set -u

source_dir=/tmp/audit-work/source
mutation_dir=/tmp/audit-work/tests/body-mutation
definition="$mutation_dir/mutated-kompiled"
status=0

print_command() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
}

run() {
  print_command "$@"
  "$@"
  rc=$?
  printf 'EXIT: %d\n' "$rc"
  if [[ "$rc" -ne 0 ]]; then
    status=1
  fi
}

printf '%s\n' '$ tr -d "[:space:]" < solution.mpy; sed -n "9,20p" verification.k | tr -d "[:space:]" (constructor-token comparison)'
tr -d '[:space:]' < "$source_dir/solution.mpy" > /tmp/audit-work/tests/submitted-program.normalized
sed -n '9,20p' "$source_dir/verification.k" \
  | tr -d '[:space:]' > /tmp/audit-work/tests/solutionProgram-rhs.normalized
cmp -s \
  /tmp/audit-work/tests/submitted-program.normalized \
  /tmp/audit-work/tests/solutionProgram-rhs.normalized
rc=$?
printf 'EXIT: %d\n' "$rc"
printf 'submitted_normalized='
sed -n '1p' /tmp/audit-work/tests/submitted-program.normalized
printf 'claim_rhs_normalized='
sed -n '1p' /tmp/audit-work/tests/solutionProgram-rhs.normalized
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

run mkdir -p "$mutation_dir"
run cp -- "$source_dir/semantic.k" "$mutation_dir/semantic.k"
run cp -- /audit-output/evidence/stage4/verification-body-mutated.k "$mutation_dir/verification.k"
run cp -- "$source_dir/spec.k" "$mutation_dir/spec.k"
run rm -rf -- "$definition"

run kompile "$mutation_dir/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition "$definition"

print_command kprove "$mutation_dir/spec.k" \
  --definition "$definition" \
  --spec-module SPEC \
  --claims UNIVERSAL-PROGRAM-REDUCTION
output=$(kprove "$mutation_dir/spec.k" \
  --definition "$definition" \
  --spec-module SPEC \
  --claims UNIVERSAL-PROGRAM-REDUCTION 2>&1)
rc=$?
printf '%s\n' "$output"
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -eq 0 ]]; then
  printf '%s\n' 'EXPECTED_NONZERO: false'
  status=1
else
  printf '%s\n' 'EXPECTED_NONZERO: true'
fi
if printf '%s\n' "$output" | rg -q 'evalList|WarnStuckClaimState|cannot be rewritten'; then
  printf '%s\n' 'EXPECTED_BODY_RESIDUAL: true'
else
  printf '%s\n' 'EXPECTED_BODY_RESIDUAL: false'
  status=1
fi

run cp -- /audit-output/evidence/stage4/audit-universal-target.k \
  "$source_dir/audit-universal-target.k"

print_command kprove "$source_dir/audit-universal-target.k" \
  --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module AUDIT-UNIVERSAL-TARGET \
  --claims AUDIT-UNIVERSAL-TARGET
output=$(kprove "$source_dir/audit-universal-target.k" \
  --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module AUDIT-UNIVERSAL-TARGET \
  --claims AUDIT-UNIVERSAL-TARGET 2>&1)
rc=$?
printf '%s\n' "$output"
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -eq 0 ]]; then
  printf '%s\n' 'EXPECTED_UNPROVED_UNIVERSAL: false'
  status=1
else
  printf '%s\n' 'EXPECTED_UNPROVED_UNIVERSAL: true'
fi
if printf '%s\n' "$output" | rg -q 'evalComp|WarnStuckClaimState|cannot be rewritten'; then
  printf '%s\n' 'EXPECTED_SYMBOLIC_LIST_RESIDUAL: true'
else
  printf '%s\n' 'EXPECTED_SYMBOLIC_LIST_RESIDUAL: false'
  status=1
fi

exit "$status"
