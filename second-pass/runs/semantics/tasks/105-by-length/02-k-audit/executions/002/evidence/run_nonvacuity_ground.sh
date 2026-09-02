#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/105-by-length/recon
overall=0
cp /audit-output/evidence/spec-vacuity-ground.k "$scratch/spec-vacuity-ground.k"

printf 'SATISFYING_WITNESS: IS = .IntSeq (Python input []); true result []; mutated destination ["Zero"]\n'
printf 'COMMAND (build only): cd %s && kprove spec-vacuity-ground.k --definition verification-kompiled --spec-module BY-LENGTH-SPEC-VACUITY-GROUND --dry-run\n' "$scratch"
(
  cd "$scratch" || exit 90
  kprove spec-vacuity-ground.k \
    --definition verification-kompiled \
    --spec-module BY-LENGTH-SPEC-VACUITY-GROUND \
    --dry-run
)
build_rc=$?
printf 'MUTATION_BUILD_EXIT_STATUS: %s\n' "$build_rc"
if (( build_rc != 0 )); then
  overall=1
fi

if (( build_rc == 0 )); then
  printf 'COMMAND (expected proof failure): cd %s && kprove spec-vacuity-ground.k --definition verification-kompiled --spec-module BY-LENGTH-SPEC-VACUITY-GROUND\n' "$scratch"
  (
    cd "$scratch" || exit 90
    set -o pipefail
    kprove spec-vacuity-ground.k \
      --definition verification-kompiled \
      --spec-module BY-LENGTH-SPEC-VACUITY-GROUND \
      2>&1 | tee spec-vacuity-ground.stdout
  )
  prove_rc=$?
  if rg 'WarnStuckClaimState' "$scratch/spec-vacuity-ground.stdout" >/dev/null; then
    stuck_rc=0
  else
    stuck_rc=1
  fi
  if rg -U '<k>\s*list \( \.ValSeq \)' "$scratch/spec-vacuity-ground.stdout" >/dev/null; then
    residual_rc=0
  else
    residual_rc=1
  fi
else
  prove_rc=99
  stuck_rc=99
  residual_rc=99
fi
printf 'MUTATION_KPROVE_EXIT_STATUS_EXPECTED_NONZERO: %s\n' "$prove_rc"
printf 'MUTATION_STUCK_CHECK_EXIT_STATUS: %s\n' "$stuck_rc"
printf 'MUTATION_EMPTY_RESULT_RESIDUAL_CHECK_EXIT_STATUS: %s\n' "$residual_rc"
if (( prove_rc == 0 || stuck_rc != 0 || residual_rc != 0 )); then
  overall=1
fi

printf 'EXIT_STATUS: %s\n' "$overall"
exit "$overall"
