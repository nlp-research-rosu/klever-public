#!/usr/bin/env bash
set -u

status=0
scratch=/tmp/audit-work/reconstruction
bridge_definition="$scratch/bridge-audit-kompiled"
body_definition="$scratch/body-audit-kompiled"

printf 'COMMAND: bash /audit-output/evidence/05_adequacy_extensions.sh\n'

printf 'STAGE: constructor-level program pinning through the K parser and evaluator\n'
printf 'RUN: kast submitted solution.mpy as Module using VERIFICATION syntax\n'
(
  cd "$scratch" || exit 98
  kast solution.mpy \
    --definition fresh-verification-kompiled \
    --module VERIFICATION \
    --sort Module \
    --output kore \
    --output-file solution.parsed.kore
)
solution_kast_status=$?
printf 'EXIT submitted constructor parse: %d\n' "$solution_kast_status"

printf 'RUN: kast largestSmallestModule as Module using VERIFICATION syntax\n'
(
  cd "$scratch" || exit 98
  kast \
    --expression largestSmallestModule \
    --definition fresh-verification-kompiled \
    --module VERIFICATION \
    --sort Module \
    --output kore \
    --output-file macro.parsed.kore
)
macro_kast_status=$?
printf 'EXIT proof-module constructor parse: %d\n' "$macro_kast_status"

printf 'RUN: krun parsed submitted module with the fresh Haskell proof definition\n'
(
  cd "$scratch" || exit 98
  krun solution.parsed.kore \
    --parser cat \
    --definition fresh-verification-kompiled \
    --output json \
    --output-file solution.final.json
)
solution_krun_status=$?
printf 'EXIT submitted module evaluation: %d\n' "$solution_krun_status"

printf 'RUN: krun parsed proof module with the fresh Haskell proof definition\n'
(
  cd "$scratch" || exit 98
  krun macro.parsed.kore \
    --parser cat \
    --definition fresh-verification-kompiled \
    --output json \
    --output-file macro.final.json
)
macro_krun_status=$?
printf 'EXIT proof module evaluation: %d\n' "$macro_krun_status"

printf 'RUN: cmp final constructor configurations\n'
cmp "$scratch/solution.final.json" "$scratch/macro.final.json"
pinning_status=$?
printf 'EXIT constructor-level pinning comparison: %d\n' "$pinning_status"
sha256sum "$scratch/solution.final.json" "$scratch/macro.final.json"
cp "$scratch/solution.final.json" /audit-output/evidence/pinning-submitted-final.json
cp "$scratch/macro.final.json" /audit-output/evidence/pinning-proof-final.json
if [[ "$solution_kast_status" -ne 0 || "$macro_kast_status" -ne 0 || \
      "$solution_krun_status" -ne 0 || "$macro_krun_status" -ne 0 || \
      "$pinning_status" -ne 0 ]]; then
  status=1
fi

printf 'STAGE: satisfiable entry and loop witnesses with ground substitution\n'
printf 'RUN: python3 /audit-output/evidence/claim_witness.py\n'
python3 /audit-output/evidence/claim_witness.py
witness_status=$?
printf 'EXIT claim witnesses: %d\n' "$witness_status"
if [[ "$witness_status" -ne 0 ]]; then
  status=1
fi

printf 'STAGE: bridge-free universal connection theorem\n'
if [[ -e "$bridge_definition" ]]; then
  printf 'FAIL fresh bridge output path already exists\n'
  exit 2
fi
cp /audit-output/evidence/bridge-base.k "$scratch/bridge-base.k"
cp /audit-output/evidence/bridge-spec.k "$scratch/bridge-spec.k"
cp /audit-output/evidence/bridge-bad-spec.k "$scratch/bridge-bad-spec.k"
cp /audit-output/evidence/bridge-unrefined-spec.k "$scratch/bridge-unrefined-spec.k"
printf 'RUN: kompile bridge-base.k without candidate verification.k or its priority bridge\n'
(
  cd "$scratch" || exit 98
  kompile bridge-base.k \
    --backend haskell \
    --main-module BRIDGE-BASE \
    --syntax-module MPY-SYNTAX \
    --output-definition bridge-audit-kompiled
)
bridge_build_status=$?
printf 'EXIT bridge-free kompile: %d\n' "$bridge_build_status"
if [[ "$bridge_build_status" -ne 0 ]]; then
  status=1
fi

printf 'RUN: kprove bridge-spec.k --definition bridge-audit-kompiled --spec-module BRIDGE-SPEC\n'
(
  cd "$scratch" || exit 98
  kprove bridge-spec.k \
    --definition bridge-audit-kompiled \
    --spec-module BRIDGE-SPEC
)
bridge_proof_status=$?
printf 'EXIT bridge connection proof: %d\n' "$bridge_proof_status"
if [[ "$bridge_proof_status" -ne 0 ]]; then
  status=1
fi

printf 'RUN EXPECTED BACKEND LIMITATION: Val-plus-isInt formulation of the same theorem\n'
(
  cd "$scratch" || exit 98
  kprove bridge-unrefined-spec.k \
    --definition bridge-audit-kompiled \
    --spec-module BRIDGE-UNREFINED-SPEC 2>&1 \
    | sed -n '1,220p'
  exit "${PIPESTATUS[0]}"
)
bridge_unrefined_status=$?
printf 'EXIT unrefined connection proof: %d (expected nonzero V=intValue(V) residual)\n' "$bridge_unrefined_status"
if [[ "$bridge_unrefined_status" -eq 0 ]]; then
  status=1
fi

printf 'RUN EXPECTED FAILURE: wrong yielded value with explicit suffix\n'
(
  cd "$scratch" || exit 98
  kprove bridge-bad-spec.k \
    --definition bridge-audit-kompiled \
    --spec-module BRIDGE-BAD-SPEC 2>&1 \
    | sed -n '1,260p'
  exit "${PIPESTATUS[0]}"
)
bridge_bad_status=$?
printf 'EXIT wrong-yield proof: %d (expected nonzero)\n' "$bridge_bad_status"
if [[ "$bridge_bad_status" -eq 0 ]]; then
  status=1
fi

printf 'STAGE: body-sensitivity mutation changes the term executed by the entry claim\n'
cp "$scratch/verification.k" /audit-output/evidence/body-mutation-verification.k
sed -i \
  's/Assign(Name("smallest_positive"), Int(0))/Assign(Name("smallest_positive"), Int(1))/' \
  /audit-output/evidence/body-mutation-verification.k
mutation_count=$(rg -F -c 'Assign(Name("smallest_positive"), Int(1))' \
  /audit-output/evidence/body-mutation-verification.k)
printf 'INFO mutation occurrence count=%s expected=1\n' "$mutation_count"
if [[ "$mutation_count" -ne 1 ]]; then
  status=1
fi
cp "$scratch/spec.k" /audit-output/evidence/body-mutation-spec.k
sed -i \
  's/requires "verification.k"/requires "body-mutation-verification.k"/' \
  /audit-output/evidence/body-mutation-spec.k
cp /audit-output/evidence/body-mutation-verification.k "$scratch/body-mutation-verification.k"
cp /audit-output/evidence/body-mutation-spec.k "$scratch/body-mutation-spec.k"

if [[ -e "$body_definition" ]]; then
  printf 'FAIL fresh body-mutation output path already exists\n'
  exit 2
fi
printf 'RUN: kompile body-mutation-verification.k\n'
(
  cd "$scratch" || exit 98
  kompile body-mutation-verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition body-audit-kompiled
)
body_build_status=$?
printf 'EXIT body-mutation kompile: %d\n' "$body_build_status"
if [[ "$body_build_status" -ne 0 ]]; then
  status=1
fi

printf 'RUN EXPECTED FAILURE: kprove entry theorem after material body mutation\n'
(
  cd "$scratch" || exit 98
  timeout 180s kprove body-mutation-spec.k \
    --definition body-audit-kompiled \
    --spec-module SPEC 2>&1 \
    | sed -n '1,320p'
  exit "${PIPESTATUS[0]}"
)
body_proof_status=$?
printf 'EXIT body-mutation proof: %d (expected proof failure, not 0 or timeout 124)\n' "$body_proof_status"
if [[ "$body_proof_status" -eq 0 || "$body_proof_status" -eq 124 ]]; then
  status=1
fi

printf 'FINAL EXIT: %d\n' "$status"
exit "$status"
