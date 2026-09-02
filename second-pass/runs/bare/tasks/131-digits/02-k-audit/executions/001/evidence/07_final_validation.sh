#!/usr/bin/env bash
set -u

failures=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then failures=1; fi
  return 0
}

printf 'AUDIT STAGE 7: FINAL ARTIFACT VALIDATION\n'
run tail -2 /audit-output/REVIEW.md
run test "$(tail -2 /audit-output/REVIEW.md | sed -n '1p')" = \
  'VERDICT: CONCERNS'
run test "$(tail -2 /audit-output/REVIEW.md | sed -n '2p')" = \
  'LEGITIMACY: LEGIT'
run test "$(grep -c '^VERDICT:' /audit-output/REVIEW.md)" -eq 1
run test "$(grep -c '^LEGITIMACY:' /audit-output/REVIEW.md)" -eq 1

run bash -n \
  /audit-output/evidence/01_provenance.sh \
  /audit-output/evidence/02_program_fidelity.sh \
  /audit-output/evidence/03_rebuild_and_prove.sh \
  /audit-output/evidence/03b_proof_targets.sh \
  /audit-output/evidence/04_adequacy_and_pinning.sh \
  /audit-output/evidence/05_static_checks.sh \
  /audit-output/evidence/06_nonvacuity.sh

run sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py

run find /audit-output/evidence -maxdepth 1 -type f \
  ! -name 07_final_validation.log -printf '%f\n'

printf '\nEvidence SHA-256 manifest (excluding this live log):\n'
find /audit-output/evidence -maxdepth 1 -type f \
  ! -name 07_final_validation.log -print0 \
  | sort -z \
  | xargs -0 sha256sum

printf '\nstage7_failures=%d\n' "$failures"
exit "$failures"
