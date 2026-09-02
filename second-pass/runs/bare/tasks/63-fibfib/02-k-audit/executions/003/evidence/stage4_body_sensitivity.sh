#!/usr/bin/env bash
set -u

mutation=/tmp/audit-work/63-fibfib/body-mutation
evidence=/audit-output/evidence
cd "$mutation" || exit 125

printf '%s\n' \
  'COMMAND: kompile --backend haskell semantic.k --main-module FIBFIB --syntax-module FIBFIB-SYNTAX --output-definition body-mut-kompiled'
kompile --backend haskell semantic.k \
  --main-module FIBFIB \
  --syntax-module FIBFIB-SYNTAX \
  --output-definition body-mut-kompiled \
  >"$evidence/stage4_body_mutation_build.log" 2>&1
build_status=$?
printf 'BUILD_EXIT: %s\n' "$build_status"
sed -n '1,260p' "$evidence/stage4_body_mutation_build.log"
if (( build_status != 0 )); then exit 1; fi

printf '%s\n' \
  'COMMAND: timeout 120s kprove spec.k --definition body-mut-kompiled --spec-module FIBFIB-SPEC -w all'
timeout 120s kprove spec.k \
  --definition body-mut-kompiled \
  --spec-module FIBFIB-SPEC \
  -w all >"$evidence/stage4_body_mutation_kprove.log" 2>&1
proof_status=$?
printf 'PROOF_EXIT: %s\n' "$proof_status"
sed -n '1,360p' "$evidence/stage4_body_mutation_kprove.log"

if (( proof_status == 0 )); then
  printf '%s\n' 'UNEXPECTED: body mutation proved'
  exit 1
fi
if (( proof_status == 124 )); then
  printf '%s\n' 'UNEXPECTED: body mutation timed out'
  exit 1
fi
if ! grep -q 'WarnStuckClaimState' "$evidence/stage4_body_mutation_kprove.log"; then
  printf '%s\n' 'UNEXPECTED: failure was not a stuck reachability obligation'
  exit 1
fi
printf '%s\n' 'EXPECTED_BODY_SENSITIVITY_FAILURE=true'
exit 0
