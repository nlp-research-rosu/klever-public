#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

SCRATCH=/tmp/audit-work/candidate
DEF="$SCRATCH/verification-kompiled"

run python3 /audit-output/evidence/04_extract_entry.py
python3 /audit-output/evidence/04_extract_entry.py --program-surface > "$SCRATCH/audit-entry-program.mpy"
printf '\n$ python3 /audit-output/evidence/04_extract_entry.py --program-surface > %s/audit-entry-program.mpy\n' "$SCRATCH"
printf '[exit %d]\n' "$?"

run kast --definition "$SCRATCH/runtime-kompiled" \
  --module MPY-SYNTAX --sort Module --output json \
  --output-file "$SCRATCH/solution.kast.json" \
  "$SCRATCH/solution.mpy"
run kast --definition "$SCRATCH/runtime-kompiled" \
  --module MPY-SYNTAX --sort Module --output json \
  --output-file "$SCRATCH/entry-program.kast.json" \
  "$SCRATCH/audit-entry-program.mpy"
run cmp -s "$SCRATCH/solution.kast.json" "$SCRATCH/entry-program.kast.json"
run sha256sum "$SCRATCH/solution.kast.json" "$SCRATCH/entry-program.kast.json"
run diff -u "$SCRATCH/solution.kast.json" "$SCRATCH/entry-program.kast.json"

run cp /audit-output/evidence/04_ground_spec.k "$SCRATCH/audit-ground-spec.k"
run kprove "$SCRATCH/audit-ground-spec.k" \
  --definition "$DEF" \
  --spec-module AUDIT-GROUND-SPEC
run python3 /audit-output/evidence/04_witnesses.py
