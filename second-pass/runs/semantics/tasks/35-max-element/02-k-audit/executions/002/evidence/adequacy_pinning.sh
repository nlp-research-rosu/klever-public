#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work/work || exit 2

run python3 /audit-output/evidence/pinning_check.py

printf '\nGround witness FIRST=1, REST=iCons(2,iCons(3,.IntSeq)):\n'
run kprove ground-witness.k \
  --definition verification-kompiled \
  --spec-module GROUND-WITNESS

printf '\nIndependent Python values for the corresponding ordinary list [1,2,3]:\n'
run python3 -c 'import canonical, solution; x=[1,2,3]; print("canonical", canonical.max_element(x)); print("candidate", solution.max_element(x))'

printf '\nBody-sensitivity mutation: change the executed constructor body to return 0.\n'
run kompile verification-body-mutated.k \
  --backend haskell \
  --main-module MAX-ELEMENT-VERIFICATION-BODY-MUTATED \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutated-kompiled
run kprove spec-body-mutated.k \
  --definition body-mutated-kompiled \
  --spec-module SPEC-BODY-MUTATED
