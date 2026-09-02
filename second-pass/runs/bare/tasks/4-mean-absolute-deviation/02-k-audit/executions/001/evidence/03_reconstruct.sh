#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction

run() {
  local description="$1"
  shift
  printf '\nCOMMAND (%s):' "$description"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT STATUS: %d\n' "$status"
  return "$status"
}

printf 'AUDIT STAGE 3: fresh semantics and proof reconstruction\n'
printf 'K TOOL VERSIONS\n'
run "kompile version" kompile --version
run "krun version" krun --version
run "kprove version" kprove --version

if [[ -e "$scratch/semantic-kompiled" || -e "$scratch/verification-kompiled" ]]; then
  printf 'REFUSING TO REUSE EXISTING SCRATCH COMPILED DEFINITIONS\n'
  exit 90
fi

cd "$scratch" || exit 91

run "fresh concrete semantics build from semantic.k" \
  kompile semantic.k \
    --backend llvm \
    --main-module SEMANTIC \
    --syntax-module MPY-SYNTAX \
    --output-definition semantic-kompiled
concrete_build_status=$?

run "concrete normal example [1,2,3,4]" \
  krun solution.mpy \
    --definition semantic-kompiled \
    -cARGS='nums(rat(1,1),rat(2,1),rat(3,1),rat(4,1))'
normal_status=$?

run "concrete singleton boundary [5]" \
  krun solution.mpy \
    --definition semantic-kompiled \
    -cARGS='nums(rat(5,1))'
singleton_status=$?

run "concrete mixed-sign example [-2,0,2]" \
  krun solution.mpy \
    --definition semantic-kompiled \
    -cARGS='nums(rat(-2,1),rat(0,1),rat(2,1))'
mixed_status=$?

run "concrete fractional example [1/2,3/2]" \
  krun solution.mpy \
    --definition semantic-kompiled \
    -cARGS='nums(rat(1,2),rat(3,2))'
fraction_status=$?

run "concrete empty boundary" \
  krun solution.mpy \
    --definition semantic-kompiled \
    -cARGS='nums()'
empty_status=$?

run "concrete negative-denominator rule witness" \
  krun solution.mpy \
    --definition semantic-kompiled \
    -cARGS='nums(rat(1,-1),rat(1,1))'
negative_denominator_status=$?

run "independent Python/exact-rational oracle observations" \
  python3 /audit-output/evidence/03_python_oracle.py
oracle_status=$?

run "fresh Haskell proof-definition build from semantic.k and verification.k" \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-kompiled
proof_build_status=$?

run "independently prove every positive claim in SPEC" \
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module SPEC
proof_status=$?

printf '\nSTAGE STATUS SUMMARY\n'
printf 'concrete_build=%d normal=%d singleton=%d mixed=%d fractions=%d empty=%d negative_denominator=%d oracle=%d proof_build=%d proof=%d\n' \
  "$concrete_build_status" "$normal_status" "$singleton_status" \
  "$mixed_status" "$fraction_status" "$empty_status" \
  "$negative_denominator_status" "$oracle_status" \
  "$proof_build_status" "$proof_status"

if (( concrete_build_status || normal_status || singleton_status || mixed_status ||
      fraction_status || empty_status || negative_denominator_status ||
      oracle_status || proof_build_status || proof_status )); then
  exit 1
fi
