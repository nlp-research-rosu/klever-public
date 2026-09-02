#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction || exit 99

printf 'Witness: N=0 satisfies N>=0. Program/triangular result is 0; mutated target is 1.\n\n'

printf '$ kprove spec-vacuity-audit.k --definition verification-kompiled-audit --spec-module SUM-TO-N-SPEC-VACUITY-AUDIT --dry-run > vacuity-dry-run.kore\n'
kprove spec-vacuity-audit.k \
  --definition verification-kompiled-audit \
  --spec-module SUM-TO-N-SPEC-VACUITY-AUDIT \
  --dry-run > vacuity-dry-run.kore
rc=$?
printf '[exit %d]\n' "$rc"
wc -c vacuity-dry-run.kore
sha256sum vacuity-dry-run.kore
printf '\n'

printf '$ kprove spec-vacuity-audit.k --definition verification-kompiled-audit --spec-module SUM-TO-N-SPEC-VACUITY-AUDIT\n'
kprove spec-vacuity-audit.k \
  --definition verification-kompiled-audit \
  --spec-module SUM-TO-N-SPEC-VACUITY-AUDIT
rc=$?
printf '[exit %d]\n' "$rc"
