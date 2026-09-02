#!/usr/bin/env bash
set -u

candidate_src=/tmp/audit-work/63-fibfib/candidate-src
evidence=/audit-output/evidence
cd "$candidate_src" || exit 125

printf '%s\n' \
  'FALSE WITNESS: N=0 satisfies 0 <=Int N; actual result=0; mutated result=fibfibMath(0)+Int 1=1.'

printf '%s\n' \
  'COMMAND: kprove spec-vacuity-audit.k --definition proof-kompiled --spec-module FIBFIB-SPEC-VACUITY --dry-run -w none'
kprove spec-vacuity-audit.k \
  --definition proof-kompiled \
  --spec-module FIBFIB-SPEC-VACUITY \
  --dry-run \
  -w none >"$evidence/stage6_vacuity_dry_run.log" 2>&1
dry_status=$?
printf 'DRY_RUN_EXIT: %s\n' "$dry_status"
sed -n '1,280p' "$evidence/stage6_vacuity_dry_run.log"
if (( dry_status != 0 )); then exit 1; fi

printf '%s\n' \
  'COMMAND: timeout 120s kprove spec-vacuity-audit.k --definition proof-kompiled --spec-module FIBFIB-SPEC-VACUITY -w all'
timeout 120s kprove spec-vacuity-audit.k \
  --definition proof-kompiled \
  --spec-module FIBFIB-SPEC-VACUITY \
  -w all >"$evidence/stage6_vacuity_kprove.log" 2>&1
proof_status=$?
printf 'PROOF_EXIT: %s\n' "$proof_status"
sed -n '1,400p' "$evidence/stage6_vacuity_kprove.log"

if (( proof_status == 0 )); then
  printf '%s\n' 'UNEXPECTED: false postcondition proved'
  exit 1
fi
if (( proof_status == 124 )); then
  printf '%s\n' 'UNEXPECTED: mutation timed out'
  exit 1
fi
if ! grep -q 'WarnStuckClaimState' "$evidence/stage6_vacuity_kprove.log"; then
  printf '%s\n' 'UNEXPECTED: failure was not a stuck reachability obligation'
  exit 1
fi
if ! grep -q 'program-wrong-off-by-one' "$evidence/stage6_vacuity_kprove.log"; then
  # Some K versions report only the source range, so retain a narrower check:
  # the residual must visibly contain the off-by-one result term.
  if ! grep -Fq 'fibfibMath ( N ) +Int 1' \
    "$evidence/stage6_vacuity_kprove.log"; then
    printf '%s\n' 'UNEXPECTED: residual does not expose the off-by-one obligation'
    exit 1
  fi
fi
printf '%s\n' 'EXPECTED_FALSE_POSTCONDITION_FAILURE=true'
exit 0
