#!/usr/bin/env bash
set -uo pipefail

CASE=/tmp/audit-work/case
BUILD=/tmp/audit-work/build
LOG=/audit-output/evidence/04b-adequacy-completed.log
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
  if (( lines <= 90 )); then
    sed -n '1,90p' "$raw"
  else
    sed -n '1,50p' "$raw"
    echo "[... bounded omission: $((lines - 80)) lines ...]"
    tail -n 30 "$raw"
  fi
  echo "[end $label]"
  return 0
}

echo '$ regenerate corrected adequacy artifacts'
python3 /audit-output/evidence/make_adequacy_artifacts.py
python3 /reference/py2mpy.py "$CASE/solution-body-mutated.py" \
  > "$CASE/solution-body-mutated.mpy"
python3 /audit-output/evidence/make_adequacy_artifacts.py --finish
echo "[exit $?]"

run_bounded pinning-original-corrected \
  kprove "$CASE/pinning-original.k" \
  --definition "$BUILD/base-kompiled" \
  --spec-module PINNING-ORIGINAL

run_bounded ground-summary-corrected \
  kprove "$CASE/ground-summary.k" \
  --definition "$BUILD/base-kompiled" \
  --spec-module GROUND-SUMMARY

run_bounded witness-helper-apply-fixed-corrected \
  kprove "$CASE/bridge-witnesses.k" \
  --definition "$BUILD/inner-kompiled" \
  --spec-module WITNESS-HELPER-APPLY-BODY
run_bounded witness-helper-apply-extended-corrected \
  kprove "$CASE/bridge-witnesses.k" \
  --definition "$BUILD/helper-kompiled" \
  --spec-module WITNESS-HELPER-APPLY-BODY

run_bounded pinning-body-mutated-corrected \
  kprove "$CASE/pinning-body-mutated.k" \
  --definition "$BUILD/body-mutated-kompiled" \
  --spec-module PINNING-BODY-MUTATED

echo '$ final adequacy artifact SHA-256'
sha256sum \
  /audit-output/evidence/pinning-original.k \
  /audit-output/evidence/pinning-body-mutated.k \
  /audit-output/evidence/solution-body-mutated.py \
  /audit-output/evidence/solution-body-mutated.mpy \
  /audit-output/evidence/verification-body-mutated.k \
  /audit-output/evidence/body-mutation-spec.k \
  /audit-output/evidence/bridge-witnesses.k \
  /audit-output/evidence/ground-summary.k
echo "[exit $?]"
