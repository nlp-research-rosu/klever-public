#!/usr/bin/env bash
set -u
set -o pipefail

work=/tmp/audit-work
evidence=/audit-output/evidence
failures=0

run_logged() {
  local logfile=$1
  shift
  printf 'COMMAND:' | tee "$logfile"
  printf ' %q' "$@" | tee -a "$logfile"
  printf '\n' | tee -a "$logfile"
  "$@" 2>&1 | tee -a "$logfile"
  local status=${PIPESTATUS[0]}
  printf 'EXIT_STATUS=%s\n' "$status" | tee -a "$logfile"
  return "$status"
}

run_claim() {
  local spec_file=$1
  local definition=$2
  local spec_module=$3
  local claim_label=$4
  local short_label=${claim_label#*.}
  local logfile="${evidence}/stage3_claim_${spec_module}_${short_label}.log"
  run_logged "$logfile" \
    kprove "$spec_file" \
      --definition "$definition" \
      --spec-module "$spec_module" \
      --claims "$claim_label" \
      --color off
  local status=$?
  if (( status != 0 )) || ! grep -qx '#Top' "$logfile"; then
    printf 'CLAIM_FAILURE=%s status=%s top=%s\n' \
      "$claim_label" "$status" "$(grep -xc '#Top' "$logfile")"
    failures=$((failures + 1))
  else
    printf 'CLAIM_SUCCESS=%s status=0 top=1\n' "$claim_label"
  fi
}

cd "$work" || exit 99

run_logged "${evidence}/stage3_build_llvm.log" \
  kompile --backend llvm semantic.k \
    --main-module MPY \
    --syntax-module MPY-SYNTAX \
    --output-definition "$work/fresh-semantic-kompiled"
build_llvm=$?
(( build_llvm == 0 )) || failures=$((failures + 1))

for n in 0 1 2 3 4 5 6; do
  logfile="${evidence}/stage3_krun_n${n}.log"
  run_logged "$logfile" \
    krun "$work/solution.mpy" \
      --definition "$work/fresh-semantic-kompiled" \
      -cN="$n" \
      --output pretty
  status=$?
  expected=$(python3 -c \
    'import sys; sys.path.insert(0, "/tmp/audit-work"); from solution import prime_fib; print(prime_fib(int(sys.argv[1])))' \
    "$n")
  actual=$(awk '
    /^[[:space:]]*<result>[[:space:]]*$/ {
      getline
      gsub(/[[:space:]]/, "")
      print
      exit
    }
  ' "$logfile")
  printf 'PYTHON_EXPECTED=%s\nK_RESULT=%s\nCOMPARE=%s\n' \
    "$expected" "$actual" "$([[ "$actual" == "$expected" ]] && printf MATCH || printf MISMATCH)" \
    | tee -a "$logfile"
  if (( status != 0 )) || [[ "$actual" != "$expected" ]]; then
    failures=$((failures + 1))
  fi
done

run_logged "${evidence}/stage3_build_concrete_haskell.log" \
  kompile --backend haskell verification.k \
    --main-module PRIME-FIB-PROGRAM \
    --syntax-module PRIME-FIB-PROGRAM \
    --output-definition "$work/fresh-concrete-kompiled"
build_concrete=$?
(( build_concrete == 0 )) || failures=$((failures + 1))

if (( build_concrete == 0 )); then
  for label in concrete-1 concrete-2 concrete-3 concrete-4 concrete-5; do
    run_claim "$work/concrete-spec.k" "$work/fresh-concrete-kompiled" \
      CONCRETE-SPEC "CONCRETE-SPEC.${label}"
  done
fi

run_logged "${evidence}/stage3_build_verification_haskell.log" \
  kompile --backend haskell verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition "$work/fresh-verification-kompiled"
build_verification=$?
(( build_verification == 0 )) || failures=$((failures + 1))

if (( build_verification == 0 )); then
  for label in prime-fib-correct example-1 example-2 example-3 example-4 example-5; do
    run_claim "$work/spec.k" "$work/fresh-verification-kompiled" \
      SPEC "SPEC.${label}"
  done
fi

printf 'build_llvm=%s\nbuild_concrete=%s\nbuild_verification=%s\nfailures=%s\n' \
  "$build_llvm" "$build_concrete" "$build_verification" "$failures"
if (( failures != 0 )); then
  exit 1
fi
printf 'SCRIPT_EXIT=0\n'
