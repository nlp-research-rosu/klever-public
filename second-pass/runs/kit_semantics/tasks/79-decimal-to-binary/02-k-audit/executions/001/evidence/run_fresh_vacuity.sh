#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/79-audit/source
cd "$scratch" || exit 1

echo '$ cp /tmp/audit-work/79-audit/source/spec-fresh-vacuity.k /audit-output/evidence/spec-fresh-vacuity.k'
cp "$scratch/spec-fresh-vacuity.k" \
  /audit-output/evidence/spec-fresh-vacuity.k
copy_status=$?
echo "COPY_EXIT_STATUS=$copy_status"

echo '$ kprove spec-fresh-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-FRESH-VACUITY --dry-run'
kprove spec-fresh-vacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-FRESH-VACUITY \
  --dry-run \
  > "$scratch/fresh-vacuity-dry-run.raw.log" 2>&1
dry_status=$?
echo "DRY_RUN_EXIT_STATUS=$dry_status"
echo 'DRY_RUN_OUTPUT_HEAD'
sed -n '1,20p' "$scratch/fresh-vacuity-dry-run.raw.log"
echo 'DRY_RUN_OUTPUT_TAIL'
tail -20 "$scratch/fresh-vacuity-dry-run.raw.log"

echo '$ kprove spec-fresh-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-FRESH-VACUITY'
kprove spec-fresh-vacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-FRESH-VACUITY \
  > "$scratch/fresh-vacuity-proof.raw.log" 2>&1
proof_status=$?
echo "MUTATED_KPROVE_EXIT_STATUS=$proof_status"
sed -n '1,260p' "$scratch/fresh-vacuity-proof.raw.log"

echo '$ rg -n "WarnStuckClaimState|100.*98.*49.*48|100.*98.*49.*49" fresh-vacuity-proof.raw.log'
rg -n \
  'WarnStuckClaimState|100.*98.*49.*48|100.*98.*49.*49' \
  "$scratch/fresh-vacuity-proof.raw.log"
residual_status=$?
echo "EXPECTED_RESIDUAL_SEARCH_EXIT_STATUS=$residual_status"

if (( copy_status || dry_status )); then
  echo 'ERROR: fresh mutation did not build successfully' >&2
  exit 1
fi
if (( proof_status == 0 )); then
  echo 'ERROR: false fresh mutation unexpectedly proved' >&2
  exit 1
fi
if (( residual_status != 0 )); then
  echo 'ERROR: proof failed without the expected stuck-result residual' >&2
  exit 1
fi
echo 'FRESH_NON_VACUITY=PASS'
