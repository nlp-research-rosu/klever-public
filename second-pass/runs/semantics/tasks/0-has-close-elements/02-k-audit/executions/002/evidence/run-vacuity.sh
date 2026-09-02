#!/usr/bin/env bash
set -uo pipefail

CASE=/tmp/audit-work/case
BUILD=/tmp/audit-work/build
LOG=/audit-output/evidence/06-fresh-non-vacuity.log
cp /audit-output/evidence/spec-vacuity.k "$CASE/spec-vacuity.k"
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
  if (( lines <= 120 )); then
    sed -n '1,120p' "$raw"
  else
    sed -n '1,70p' "$raw"
    echo "[... bounded omission: $((lines - 110)) lines ...]"
    tail -n 40 "$raw"
  fi
  echo "[end $label]"
  return 0
}

run_bounded vacuity-dry-run \
  kprove "$CASE/spec-vacuity.k" \
  --definition "$BUILD/entry-kompiled" \
  --spec-module SPEC-VACUITY \
  --dry-run

run_bounded vacuity-proof \
  kprove "$CASE/spec-vacuity.k" \
  --definition "$BUILD/entry-kompiled" \
  --spec-module SPEC-VACUITY

echo '$ expected-failure signal counts'
echo "WarnStuckClaimState=$(grep -c WarnStuckClaimState "$BUILD/vacuity-proof.raw.log")"
echo "ProverErrors=$(grep -c '\\[Error\\] Prover' "$BUILD/vacuity-proof.raw.log")"
echo "TopLines=$(grep -c '^#Top$' "$BUILD/vacuity-proof.raw.log")"
echo "[exit 0]"
echo '$ SHA-256 mutation'
sha256sum /audit-output/evidence/spec-vacuity.k
echo "[exit $?]"
