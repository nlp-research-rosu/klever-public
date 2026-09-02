#!/usr/bin/env bash
set -uo pipefail

CASE=/tmp/audit-work/case
BUILD=/tmp/audit-work/build
LOG=/audit-output/evidence/04c-pinning-completed.log
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

echo '$ generate pinning artifacts (internally: kast exact .mpy to normalized constructor term)'
python3 /audit-output/evidence/make_adequacy_artifacts.py
python3 /reference/py2mpy.py "$CASE/solution-body-mutated.py" \
  > "$CASE/solution-body-mutated.mpy"
python3 /audit-output/evidence/make_adequacy_artifacts.py --finish
echo "[exit $?]"

run_bounded pinning-original-final \
  kprove "$CASE/pinning-original.k" \
  --definition "$BUILD/base-kompiled" \
  --spec-module PINNING-ORIGINAL

run_bounded ground-summary-final \
  kprove "$CASE/ground-summary.k" \
  --definition "$BUILD/base-kompiled" \
  --spec-module GROUND-SUMMARY

run_bounded pinning-body-mutated-final \
  kprove "$CASE/pinning-body-mutated.k" \
  --definition "$BUILD/body-mutated-kompiled" \
  --spec-module PINNING-BODY-MUTATED

echo '$ pinning artifact SHA-256'
sha256sum \
  /audit-output/evidence/solution.normalized.kterm \
  /audit-output/evidence/pinning-original.k \
  /audit-output/evidence/solution-body-mutated.normalized.kterm \
  /audit-output/evidence/pinning-body-mutated.k \
  /audit-output/evidence/ground-summary.k
echo "[exit $?]"
