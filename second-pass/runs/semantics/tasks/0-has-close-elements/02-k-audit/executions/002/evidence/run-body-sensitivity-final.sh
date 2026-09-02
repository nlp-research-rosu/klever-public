#!/usr/bin/env bash
set -uo pipefail

CASE=/tmp/audit-work/case
BUILD=/tmp/audit-work/build
LOG=/audit-output/evidence/04d-body-sensitivity-final.log
exec > >(tee "$LOG") 2>&1

run_bounded() {
  local label=$1
  shift
  local raw="$BUILD/${label}.raw.log"
  echo "\$ $*"
  "$@" >"$raw" 2>&1
  local status=$?
  local lines
  lines=$(wc -l <"$raw")
  echo "[exit $status; raw_lines=$lines]"
  if (( lines <= 80 )); then
    sed -n '1,80p' "$raw"
  else
    sed -n '1,45p' "$raw"
    echo "[... bounded omission: $((lines - 70)) lines ...]"
    tail -n 25 "$raw"
  fi
  echo "[end $label]"
  return 0
}

echo '$ diff normalized original and body-mutated constructor terms'
diff -u \
  /audit-output/evidence/solution.normalized.kterm \
  /audit-output/evidence/solution-body-mutated.normalized.kterm
echo "[exit $?; expected nonzero because the executed body changed]"

run_bounded body-mutated-pinning-final \
  kprove "$CASE/pinning-body-mutated.k" \
  --definition "$BUILD/body-mutated-kompiled" \
  --spec-module PINNING-BODY-MUTATED

run_bounded body-mutated-false-program-proof-final \
  kprove "$CASE/body-mutation-spec.k" \
  --definition "$BUILD/body-mutated-kompiled" \
  --spec-module BODY-MUTATION-SPEC

run_bounded body-mutated-python-witness-final \
  python3 /audit-output/evidence/check_body_mutation.py
