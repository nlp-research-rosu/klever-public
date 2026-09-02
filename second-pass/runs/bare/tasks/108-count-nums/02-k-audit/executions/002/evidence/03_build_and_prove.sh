#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT_STATUS=%s\n" "$status"' EXIT
set -x

SCRATCH=/tmp/audit-work/108-count-nums
cd "$SCRATCH"
cp /audit-output/evidence/spec-labeled.k "$SCRATCH/spec-labeled.k"
test ! -e semantic-kompiled
test ! -e verification-kompiled

failures=0
run_positive() {
  description=$1
  shift
  printf "BEGIN_POSITIVE %s\n" "$description"
  "$@"
  status=$?
  printf "END_POSITIVE %s EXIT_STATUS=%s\n" "$description" "$status"
  if [[ "$status" -ne 0 ]]; then
    failures=$((failures + 1))
  fi
}

run_pipe_positive() {
  description=$1
  expected=$2
  shift 2
  printf "BEGIN_POSITIVE %s\n" "$description"
  "$@" | grep -F "$expected"
  statuses=("${PIPESTATUS[@]}")
  printf "PIPE_STATUSES %s %s\n" "${statuses[0]}" "${statuses[1]}"
  status=0
  if [[ "${statuses[0]}" -ne 0 || "${statuses[1]}" -ne 0 ]]; then
    status=1
    failures=$((failures + 1))
  fi
  printf "END_POSITIVE %s EXIT_STATUS=%s\n" "$description" "$status"
}

run_positive llvm_build kompile semantic.k \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition semantic-kompiled

run_pipe_positive krun_empty 'IntV ( 0 ) ~> .K' \
  krun solution.mpy --definition semantic-kompiled -cARG='list()'
run_pipe_positive krun_negative_recursive_boundary 'IntV ( 0 ) ~> .K' \
  krun solution.mpy --definition semantic-kompiled -cARG='list(-10)'
run_pipe_positive krun_negative_base_boundary 'IntV ( 0 ) ~> .K' \
  krun solution.mpy --definition semantic-kompiled -cARG='list(-9)'
run_pipe_positive krun_positive_base_boundary 'IntV ( 1 ) ~> .K' \
  krun solution.mpy --definition semantic-kompiled -cARG='list(9)'
run_pipe_positive krun_positive_recursive_boundary 'IntV ( 1 ) ~> .K' \
  krun solution.mpy --definition semantic-kompiled -cARG='list(10)'
run_pipe_positive krun_documented_mixed 'IntV ( 1 ) ~> .K' \
  krun solution.mpy --definition semantic-kompiled -cARG='list(-1, 11, -11)'
run_pipe_positive krun_all_used_branches 'IntV ( 2 ) ~> .K' \
  krun solution.mpy --definition semantic-kompiled \
  -cARG='list(-123, -100, -99, 0, 10)'

run_positive haskell_build kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition verification-kompiled

run_positive original_all_claims kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

run_positive labeled_all_claims kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module SPEC-LABELED

for label in \
  digit-helper \
  count-empty \
  count-positive-head \
  count-nonpositive-head \
  entry-empty \
  entry-positive-head \
  entry-nonpositive-head
do
  run_positive "claim_${label}" \
    kprove spec-labeled.k \
      --definition verification-kompiled \
      --spec-module SPEC-LABELED \
      --claims "SPEC-LABELED.${label}"
done

printf "TOTAL_POSITIVE_FAILURES=%s\n" "$failures"
exit "$failures"
