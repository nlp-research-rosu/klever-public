#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd /tmp/audit-work/reconstruction || exit 125
run test ! -e /candidate/spec-vacuity.k
run cp /audit-output/evidence/spec-vacuity.k spec-vacuity.k
run python3 -c \
  'import importlib.util; p="solution.py"; s=importlib.util.spec_from_file_location("candidate",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print({"witness": "", "actual": m.digitSum(""), "mutated_required": 1})'

# Parse/build the exact mutated target and its already-proved support claim.
run kprove spec-vacuity.k \
  --definition audit-proof-haskell-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.mutated-entry,SPEC-VACUITY.loop \
  --trusted SPEC-VACUITY.loop \
  --dry-run

# Expected semantic failure: a stuck final result obligation, not a parser,
# import, compilation, timeout, or unrelated crash.
run timeout 180s kprove spec-vacuity.k \
  --definition audit-proof-haskell-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.mutated-entry,SPEC-VACUITY.loop \
  --trusted SPEC-VACUITY.loop
