#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/111-histogram
proof_definition="$audit_work/verification-audit-kompiled"
mutation_definition="$audit_work/verification-body-mutation-kompiled"
overall_status=0

run_in_work_and_record() {
  printf 'COMMAND: (cd %q &&' "$audit_work"
  printf ' %q' "$@"
  printf ')\n'
  (
    cd "$audit_work" &&
    "$@"
  )
  local command_status=$?
  printf 'EXIT_STATUS: %s\n' "$command_status"
  if (( command_status != 0 )); then overall_status=1; fi
  return 0
}

run_in_work_and_record \
  kast --definition "$proof_definition" \
  --module VERIFICATION --sort Module --expand-macros --output json \
  solution.mpy --output-file solution-kast.json

run_in_work_and_record \
  kast --definition "$proof_definition" \
  --module VERIFICATION --sort Module --expand-macros --output json \
  --expression 'histogramCheck(Str("x"), DictExpr())' \
  --output-file wrapper-kast.json

printf 'COMMAND: python3 /audit-output/evidence/constructor_compare.py\n'
python3 /audit-output/evidence/constructor_compare.py
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf 'COMMAND: python3 /audit-output/evidence/claim_witnesses.py\n'
python3 /audit-output/evidence/claim_witnesses.py
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf '%s\n' \
  "COMMAND: mechanically rename VERIFICATION and change the executed increment Int(1) to Int(2)"
(
  cd "$audit_work" &&
  sed \
    -e 's/^module VERIFICATION$/module VERIFICATION-BODY-MUTATION/' \
    -e 's/BinOp("+", Subscript(Name("counts"), Name("letter")), Int(1)))/BinOp("+", Subscript(Name("counts"), Name("letter")), Int(2)))/' \
    verification.k > verification-body-mutation.k
)
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf '%s\n' \
  "COMMAND: mechanically retarget spec-labeled.k to VERIFICATION-BODY-MUTATION"
(
  cd "$audit_work" &&
  sed \
    -e 's/requires "verification.k"/requires "verification-body-mutation.k"/' \
    -e 's/^  imports VERIFICATION$/  imports VERIFICATION-BODY-MUTATION/' \
    spec-labeled.k > spec-body-mutation.k
)
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf 'COMMAND: (cd %q && diff -u verification.k verification-body-mutation.k)\n' "$audit_work"
(
  cd "$audit_work" &&
  diff -u verification.k verification-body-mutation.k
)
diff_status=$?
printf 'EXPECTED_DIFF_EXIT_STATUS: %s\n' "$diff_status"
if (( diff_status != 1 )); then overall_status=1; fi

(
  cd "$audit_work" &&
  grep -q 'Int(2)' verification-body-mutation.k &&
  ! cmp -s verification.k verification-body-mutation.k
)
command_status=$?
printf 'BODY_MUTATION_SOURCE_CHECK_EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

run_in_work_and_record \
  kompile verification-body-mutation.k \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUTATION \
  --syntax-module VERIFICATION-BODY-MUTATION \
  --output-definition "$mutation_definition"

run_in_work_and_record \
  kast --definition "$mutation_definition" \
  --module VERIFICATION-BODY-MUTATION --sort Module --expand-macros --output json \
  --expression 'histogramCheck(Str("x"), DictExpr())' \
  --output-file body-mutation-wrapper-kast.json

printf 'COMMAND: python3 /audit-output/evidence/body_mutation_compare.py\n'
python3 /audit-output/evidence/body_mutation_compare.py
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf '%s\n' \
  "COMMAND: kprove spec-body-mutation.k --definition $mutation_definition --spec-module HISTOGRAM-SPEC-LABELED --claims HISTOGRAM-SPEC-LABELED.claim-03 --warnings none"
(
  cd "$audit_work" &&
  kprove spec-body-mutation.k \
    --definition "$mutation_definition" \
    --spec-module HISTOGRAM-SPEC-LABELED \
    --claims HISTOGRAM-SPEC-LABELED.claim-03 \
    --warnings none 2>&1 | tee body-mutation-proof.raw.log
  proof_status=${PIPESTATUS[0]}
  printf 'EXPECTED_NONZERO_EXIT_STATUS: %s\n' "$proof_status"
  test "$proof_status" -ne 0 &&
    grep -q 'WarnStuckClaimState' body-mutation-proof.raw.log
)
command_status=$?
printf 'EXPECTED_FAILURE_VALIDATION_EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

exit "$overall_status"
