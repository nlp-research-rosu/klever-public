#!/usr/bin/env bash
set -u

work="/tmp/audit-work/reconstruction"
log="/audit-output/evidence/vacuity.log"
printf '%s\n' \
  'COMMAND: kprove /audit-output/evidence/spec-vacuity.k -I /tmp/audit-work/reconstruction --definition verification-kompiled --spec-module SPEC-VACUITY' \
  >"${log}"
(
  cd "${work}" &&
  kprove /audit-output/evidence/spec-vacuity.k \
    -I "${work}" \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY
) >>"${log}" 2>&1
status=$?
if grep -qx '#Top' "${log}"; then top=yes; else top=no; fi
if grep -q 'WarnStuckClaimState' "${log}"; then stuck=yes; else stuck=no; fi
printf 'PRINTED_EXACT_TOP_LINE: %s\n' "${top}" >>"${log}"
printf 'PRINTED_STUCK_CLAIM: %s\n' "${stuck}" >>"${log}"
printf 'EXIT_STATUS: %s\n' "${status}" >>"${log}"

if (( status != 0 )) && [[ "${top}" == no && "${stuck}" == yes ]]; then
  exit 0
fi
exit 1
