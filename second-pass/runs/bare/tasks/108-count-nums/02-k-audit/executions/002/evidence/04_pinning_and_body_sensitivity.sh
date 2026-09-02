#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT_STATUS=%s\n" "$status"' EXIT
set -x

SCRATCH=/tmp/audit-work/108-count-nums
cd "$SCRATCH"

kast solution.mpy \
  --definition verification-kompiled \
  --sort Program \
  --module MPY-SYNTAX \
  --expand-macros \
  --output kore \
  --output-file /audit-output/evidence/04_solution_file.kore
kast \
  --expression solutionProgram \
  --definition verification-kompiled \
  --sort Program \
  --module VERIFICATION \
  --expand-macros \
  --output kore \
  --output-file /audit-output/evidence/04_solution_macro.kore
cmp /audit-output/evidence/04_solution_file.kore \
    /audit-output/evidence/04_solution_macro.kore
sha256sum /audit-output/evidence/04_solution_file.kore \
          /audit-output/evidence/04_solution_macro.kore

python3 - <<'PY'
from canonical import count_nums as canonical
from solution import count_nums as candidate

witnesses = {
    "entry_empty": [],
    "entry_positive_head": [11],
    "entry_nonpositive_head": [-11, 11],
}
for name, values in witnesses.items():
    expected = canonical(values)
    actual = candidate(values)
    print(name, values, "canonical", expected, "candidate", actual)
    assert expected == actual
PY

krun solution.mpy --definition semantic-kompiled -cARG='list()' \
  | grep -F 'IntV ( 0 ) ~> .K'
test "${PIPESTATUS[0]}" -eq 0
krun solution.mpy --definition semantic-kompiled -cARG='list(11)' \
  | grep -F 'IntV ( 1 ) ~> .K'
test "${PIPESTATUS[0]}" -eq 0
krun solution.mpy --definition semantic-kompiled -cARG='list(-11, 11)' \
  | grep -F 'IntV ( 1 ) ~> .K'
test "${PIPESTATUS[0]}" -eq 0

MUTATED="$SCRATCH/body-mutated"
test ! -e "$MUTATED"
mkdir "$MUTATED"
cp semantic.k "$MUTATED/semantic.k"
cp solution.mpy "$MUTATED/solution.mpy"
cp spec-labeled.k "$MUTATED/spec-labeled.k"
cp /audit-output/evidence/verification-body-mutated.k "$MUTATED/verification.k"
cd "$MUTATED"

kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition verification-kompiled

kast solution.mpy \
  --definition verification-kompiled \
  --sort Program \
  --module MPY-SYNTAX \
  --expand-macros \
  --output kore \
  --output-file /audit-output/evidence/04_mutated_solution_file.kore
kast \
  --expression solutionProgram \
  --definition verification-kompiled \
  --sort Program \
  --module VERIFICATION \
  --expand-macros \
  --output kore \
  --output-file /audit-output/evidence/04_mutated_solution_macro.kore

set +e
cmp /audit-output/evidence/04_mutated_solution_file.kore \
    /audit-output/evidence/04_mutated_solution_macro.kore
cmp_status=$?
timeout --signal=TERM --kill-after=10 120 \
  kprove spec-labeled.k \
    --definition verification-kompiled \
    --spec-module SPEC-LABELED \
    --claims SPEC-LABELED.entry-empty \
  2>&1 | tee /audit-output/evidence/04_body_mutation_kprove.raw.log
proof_status=${PIPESTATUS[0]}
set -e

printf "EXPECTED_KORE_MISMATCH_STATUS=%s\n" "$cmp_status"
printf "EXPECTED_PROOF_FAILURE_STATUS=%s\n" "$proof_status"
test "$cmp_status" -eq 1
test "$proof_status" -ne 0
grep -F 'WarnStuckClaimState' /audit-output/evidence/04_body_mutation_kprove.raw.log
grep -F 'IntV ( 1 )' /audit-output/evidence/04_body_mutation_kprove.raw.log
