#!/usr/bin/env bash
set -uo pipefail

SCRATCH=/tmp/audit-work/reviewer-002/scratch
MASTER=/audit-output/evidence/03-clean-reconstruction.log
: > "$MASTER"

run_logged() {
  output_log=$1
  shift
  printf '$ (cd %s &&' "$SCRATCH" >> "$MASTER"
  printf ' %q' "$@" >> "$MASTER"
  printf ')\n' >> "$MASTER"
  (
    cd "$SCRATCH" || exit 125
    "$@"
  ) > "$output_log" 2>&1
  command_status=$?
  printf 'EXIT: %s\n' "$command_status" >> "$MASTER"
  printf 'OUTPUT: %s\n\n' "$output_log" >> "$MASTER"
  return 0
}

run_logged /audit-output/evidence/03-k-version.log kompile --version

printf '%s\n' \
  '$ (cd /tmp/audit-work/reviewer-002/scratch && python3 py2mpy.py concrete-tests.py > reviewer-concrete-tests.mpy)' \
  >> "$MASTER"
(
  cd "$SCRATCH" || exit 125
  python3 py2mpy.py concrete-tests.py > reviewer-concrete-tests.mpy
) > /audit-output/evidence/03-regenerate-concrete.log 2>&1
command_status=$?
printf 'EXIT: %s\n' "$command_status" >> "$MASTER"
printf 'OUTPUT: %s\n\n' /audit-output/evidence/03-regenerate-concrete.log >> "$MASTER"

run_logged /audit-output/evidence/03-concrete-mpy-cmp.log \
  cmp -l concrete-tests.mpy reviewer-concrete-tests.mpy
run_logged /audit-output/evidence/03-build-runtime.log \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
run_logged /audit-output/evidence/03-krun.log \
  krun reviewer-concrete-tests.mpy \
  --definition reviewer-runtime-kompiled \
  --output pretty
run_logged /audit-output/evidence/03-build-proof.log \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled

printf '%s\n' \
  '$ (cd /tmp/audit-work/reviewer-002/scratch && kprove spec-labeled.k --definition reviewer-verification-kompiled --spec-module SPEC --dry-run --emit-json-spec reviewer-spec.json --output none)' \
  >> "$MASTER"
(
  cd "$SCRATCH" || exit 125
  kprove spec-labeled.k \
    --definition reviewer-verification-kompiled \
    --spec-module SPEC \
    --dry-run \
    --emit-json-spec reviewer-spec.json \
    --output none
) > /audit-output/evidence/03-spec-dry-run.log 2>&1
command_status=$?
printf 'EXIT: %s\n' "$command_status" >> "$MASTER"
printf 'OUTPUT: %s\n\n' /audit-output/evidence/03-spec-dry-run.log >> "$MASTER"

for claim_label in \
  inner-loop \
  entry-neg5 \
  entry-0 \
  entry-50 \
  entry-78 \
  entry-79 \
  entry-100
do
  run_logged "/audit-output/evidence/03-kprove-${claim_label}.log" \
    kprove spec-labeled.k \
    --definition reviewer-verification-kompiled \
    --spec-module SPEC \
    --claims "SPEC.${claim_label}" \
    --output pretty
done

printf '%s\n' 'BOUNDED_OUTPUT_SUMMARY_BEGIN' >> "$MASTER"
for output_log in \
  /audit-output/evidence/03-k-version.log \
  /audit-output/evidence/03-regenerate-concrete.log \
  /audit-output/evidence/03-concrete-mpy-cmp.log \
  /audit-output/evidence/03-build-runtime.log \
  /audit-output/evidence/03-krun.log \
  /audit-output/evidence/03-build-proof.log \
  /audit-output/evidence/03-spec-dry-run.log \
  /audit-output/evidence/03-kprove-inner-loop.log \
  /audit-output/evidence/03-kprove-entry-neg5.log \
  /audit-output/evidence/03-kprove-entry-0.log \
  /audit-output/evidence/03-kprove-entry-50.log \
  /audit-output/evidence/03-kprove-entry-78.log \
  /audit-output/evidence/03-kprove-entry-79.log \
  /audit-output/evidence/03-kprove-entry-100.log
do
  printf '%s\n' "### $output_log" >> "$MASTER"
  sed -n '1,80p' "$output_log" >> "$MASTER"
  output_lines=$(wc -l < "$output_log")
  if [ "$output_lines" -gt 80 ]; then
    printf '%s\n' "... omitted middle; total lines=$output_lines ..." >> "$MASTER"
    tail -40 "$output_log" >> "$MASTER"
  fi
done
printf '%s\n' 'BOUNDED_OUTPUT_SUMMARY_END' >> "$MASTER"
