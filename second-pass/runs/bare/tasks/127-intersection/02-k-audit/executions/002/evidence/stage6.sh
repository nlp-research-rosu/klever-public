#!/usr/bin/env bash
set -u

source_dir=/tmp/audit-work/candidate-src
whole_definition=/tmp/audit-work/build-proof/verification-kompiled
evidence_dir=/audit-output/evidence

echo "COMMAND: cp ${evidence_dir}/spec-vacuity-fresh.k ${source_dir}/spec-vacuity-fresh.k"
cp "${evidence_dir}/spec-vacuity-fresh.k" "${source_dir}/spec-vacuity-fresh.k"
copy_status=$?
echo "EXIT: ${copy_status}"

cd "${source_dir}" || exit 90

echo "COMMAND: kprove spec-vacuity-fresh.k --definition ${whole_definition} --spec-module SPEC-VACUITY-FRESH --dry-run"
kprove spec-vacuity-fresh.k \
  --definition "${whole_definition}" \
  --spec-module SPEC-VACUITY-FRESH \
  --dry-run \
  > "${evidence_dir}/vacuity-dry-run.log" 2>&1
dry_run_status=$?
echo "EXIT: ${dry_run_status}"
sed -n '1,180p' "${evidence_dir}/vacuity-dry-run.log"

echo "COMMAND: kprove spec-vacuity-fresh.k --definition ${whole_definition} --spec-module SPEC-VACUITY-FRESH --output pretty"
kprove spec-vacuity-fresh.k \
  --definition "${whole_definition}" \
  --spec-module SPEC-VACUITY-FRESH \
  --output pretty \
  > "${evidence_dir}/vacuity-proof.log" 2>&1
proof_status=$?
stuck_count=$(rg -c 'WarnStuckClaimState' "${evidence_dir}/vacuity-proof.log" || true)
stuck_count=${stuck_count:-0}
yes_count=$(rg -c 'strVal.*"YES"' "${evidence_dir}/vacuity-proof.log" || true)
yes_count=${yes_count:-0}
echo "EXIT: ${proof_status} (expected nonzero)"
echo "STUCK_COUNT: ${stuck_count}"
echo "RESIDUAL_YES_COUNT: ${yes_count}"
sed -n '1,300p' "${evidence_dir}/vacuity-proof.log"

if [ "${copy_status}" -ne 0 ] \
   || [ "${dry_run_status}" -ne 0 ] \
   || [ "${proof_status}" -eq 0 ] \
   || [ "${stuck_count}" -lt 1 ] \
   || [ "${yes_count}" -lt 1 ]; then
  exit 1
fi
