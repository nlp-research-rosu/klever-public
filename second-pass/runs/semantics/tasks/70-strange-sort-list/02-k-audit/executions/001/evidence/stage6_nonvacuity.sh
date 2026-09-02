#!/usr/bin/env bash
set -u

work=/tmp/audit-work/recon
raw_dir="$work/raw-logs"
mkdir -p "$raw_dir"
failed=0

run_bounded() {
  local label=$1
  shift
  local raw="$raw_dir/$label.log"
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$raw" 2>&1
  local status=$?
  local lines
  lines=$(wc -l <"$raw")
  printf '[captured %d lines in %s]\n' "$lines" "$raw"
  sed -n '1,180p' "$raw"
  if (( lines > 260 )); then
    printf '[... middle omitted from bounded evidence log ...]\n'
    tail -n 80 "$raw"
  fi
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'Satisfying witness: INPUT = .ValSeq (the empty integer list).\n'
printf 'Expected result content: .ValSeq; mutated content: vCons(0, .ValSeq).\n'

run_bounded mutation_dry_run \
  kprove /audit-output/evidence/spec-vacuity-audit.k \
  -I /tmp/audit-work/recon \
  --definition /tmp/audit-work/recon/verification-kompiled \
  --spec-module AUDIT-VACUITY \
  --claims AUDIT-VACUITY.extra-result-element \
  --dry-run
dry_status=$?
if (( dry_status != 0 )); then
  printf 'UNEXPECTED: mutation did not parse/build\n'
  failed=1
fi

run_bounded mutation_proof \
  kprove /audit-output/evidence/spec-vacuity-audit.k \
  -I /tmp/audit-work/recon \
  --definition /tmp/audit-work/recon/verification-kompiled \
  --spec-module AUDIT-VACUITY \
  --claims AUDIT-VACUITY.extra-result-element
proof_status=$?
if (( proof_status == 0 )); then
  printf 'UNEXPECTED: false mutation closed\n'
  failed=1
else
  printf 'expected non-zero proof status observed\n'
fi

if rg -q 'WarnStuckClaimState' "$raw_dir/mutation_proof.log" \
  && rg -q 'implication check between the conditions has failed' "$raw_dir/mutation_proof.log" \
  && rg -Fq '#Equals' "$raw_dir/mutation_proof.log" \
  && rg -Fq 'strangePrefix' "$raw_dir/mutation_proof.log" \
  && rg -Fq 'vCons ( 0 , strangePrefix' "$raw_dir/mutation_proof.log" \
  && rg -Fq 'vCons(0, strangeResult' /audit-output/evidence/spec-vacuity-audit.k
then
  printf 'expected non-unification of real content with extra-element mutation found\n'
else
  printf 'UNEXPECTED: residual did not show the mutated return mismatch\n'
  failed=1
fi

exit "$failed"
