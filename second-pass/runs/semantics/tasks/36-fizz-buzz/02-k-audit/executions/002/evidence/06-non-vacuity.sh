#!/usr/bin/env bash
set -uo pipefail

SCRATCH=/tmp/audit-work/reviewer-002/scratch
LOG=/audit-output/evidence/06-non-vacuity.log
: > "$LOG"

run() {
  output_log=$1
  shift
  printf '$ (cd %s &&' "$SCRATCH" >> "$LOG"
  printf ' %q' "$@" >> "$LOG"
  printf ')\n' >> "$LOG"
  (
    cd "$SCRATCH" || exit 125
    "$@"
  ) > "$output_log" 2>&1
  command_status=$?
  printf 'EXIT: %s\n' "$command_status" >> "$LOG"
  printf 'OUTPUT: %s\n\n' "$output_log" >> "$LOG"
  return 0
}

run /audit-output/evidence/06-python-witness.log \
  python3 -c \
  'import canonical, solution; print("n=78 canonical=", canonical.fizz_buzz(78), "generated=", solution.fizz_buzz(78)); raise SystemExit(not (canonical.fizz_buzz(78) == solution.fizz_buzz(78) == 2))'
run /audit-output/evidence/06-mutation-dry-run.log \
  kprove /audit-output/evidence/spec-vacuity.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-entry-78 \
  -I "$SCRATCH" \
  --dry-run \
  --output none
run /audit-output/evidence/06-mutation-proof.log \
  kprove /audit-output/evidence/spec-vacuity.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-entry-78 \
  -I "$SCRATCH" \
  --output pretty
run /audit-output/evidence/06-body-mutation-dry-run.log \
  kprove /audit-output/evidence/spec-body-sensitivity.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC-BODY-SENSITIVITY \
  --claims SPEC-BODY-SENSITIVITY.mutated-body-entry-78 \
  -I "$SCRATCH" \
  --dry-run \
  --output none
run /audit-output/evidence/06-body-mutation-proof.log \
  kprove /audit-output/evidence/spec-body-sensitivity.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC-BODY-SENSITIVITY \
  --claims SPEC-BODY-SENSITIVITY.mutated-body-entry-78 \
  -I "$SCRATCH" \
  --output pretty

printf '%s\n' 'BOUNDED_OUTPUT_BEGIN' >> "$LOG"
for output_log in \
  /audit-output/evidence/06-python-witness.log \
  /audit-output/evidence/06-mutation-dry-run.log \
  /audit-output/evidence/06-mutation-proof.log \
  /audit-output/evidence/06-body-mutation-dry-run.log \
  /audit-output/evidence/06-body-mutation-proof.log
do
  printf '%s\n' "### $output_log" >> "$LOG"
  sed -n '1,120p' "$output_log" >> "$LOG"
  output_lines=$(wc -l < "$output_log")
  if [ "$output_lines" -gt 120 ]; then
    printf '%s\n' "... omitted middle; total lines=$output_lines ..." >> "$LOG"
    tail -60 "$output_log" >> "$LOG"
  fi
done
printf '%s\n' 'BOUNDED_OUTPUT_END' >> "$LOG"
