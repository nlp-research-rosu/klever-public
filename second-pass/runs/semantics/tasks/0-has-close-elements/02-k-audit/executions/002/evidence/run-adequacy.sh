#!/usr/bin/env bash
set -uo pipefail

CASE=/tmp/audit-work/case
BUILD=/tmp/audit-work/build
LOG=/audit-output/evidence/04-adequacy-and-bridges.log
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

echo '$ python3 /audit-output/evidence/make_adequacy_artifacts.py'
python3 /audit-output/evidence/make_adequacy_artifacts.py
echo "[exit $?]"

echo '$ python3 /reference/py2mpy.py /tmp/audit-work/case/solution-body-mutated.py > /tmp/audit-work/case/solution-body-mutated.mpy'
python3 /reference/py2mpy.py "$CASE/solution-body-mutated.py" \
  > "$CASE/solution-body-mutated.mpy"
echo "[exit $?]"

echo '$ python3 /audit-output/evidence/make_adequacy_artifacts.py --finish'
python3 /audit-output/evidence/make_adequacy_artifacts.py --finish
echo "[exit $?]"

run_bounded pinning-original \
  kprove "$CASE/pinning-original.k" \
  --definition "$BUILD/base-kompiled" \
  --spec-module PINNING-ORIGINAL

run_bounded ground-summary \
  kprove "$CASE/ground-summary.k" \
  --definition "$BUILD/base-kompiled" \
  --spec-module GROUND-SUMMARY

echo 'Inner arbitrary-body bridge: fixed definition must reject; extended definition closes.'
run_bounded witness-inner-fixed \
  kprove "$CASE/bridge-witnesses.k" \
  --definition "$BUILD/base-kompiled" \
  --spec-module WITNESS-INNER-BODY
run_bounded witness-inner-extended \
  kprove "$CASE/bridge-witnesses.k" \
  --definition "$BUILD/inner-kompiled" \
  --spec-module WITNESS-INNER-BODY

echo 'Helper arbitrary-closure-body bridge: fixed definition must reject; extended definition closes.'
run_bounded witness-helper-apply-fixed \
  kprove "$CASE/bridge-witnesses.k" \
  --definition "$BUILD/inner-kompiled" \
  --spec-module WITNESS-HELPER-APPLY-BODY
run_bounded witness-helper-apply-extended \
  kprove "$CASE/bridge-witnesses.k" \
  --definition "$BUILD/helper-kompiled" \
  --spec-module WITNESS-HELPER-APPLY-BODY

echo 'Helper textual-call binding bridge: fixed definition must reject; extended definition closes.'
run_bounded witness-helper-call-fixed \
  kprove "$CASE/bridge-witnesses.k" \
  --definition "$BUILD/inner-kompiled" \
  --spec-module WITNESS-HELPER-CALL-BINDING
run_bounded witness-helper-call-extended \
  kprove "$CASE/bridge-witnesses.k" \
  --definition "$BUILD/helper-kompiled" \
  --spec-module WITNESS-HELPER-CALL-BINDING

echo 'Outer arbitrary-body bridge: fixed definition must reject; extended definition closes.'
run_bounded witness-outer-fixed \
  kprove "$CASE/bridge-witnesses.k" \
  --definition "$BUILD/helper-kompiled" \
  --spec-module WITNESS-OUTER-BODY
run_bounded witness-outer-extended \
  kprove "$CASE/bridge-witnesses.k" \
  --definition "$BUILD/outer-kompiled" \
  --spec-module WITNESS-OUTER-BODY

echo 'Entry textual-call binding bridge: fixed definition must reject; extended definition closes.'
run_bounded witness-entry-fixed \
  kprove "$CASE/bridge-witnesses.k" \
  --definition "$BUILD/outer-kompiled" \
  --spec-module WITNESS-ENTRY-CALL-BINDING
run_bounded witness-entry-extended \
  kprove "$CASE/bridge-witnesses.k" \
  --definition "$BUILD/entry-kompiled" \
  --spec-module WITNESS-ENTRY-CALL-BINDING

run_bounded body-mutated-kompile \
  kompile "$CASE/verification-body-mutated.k" \
  --backend haskell \
  --main-module VERIFICATION-WITH-ENTRY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$BUILD/body-mutated-kompiled"

run_bounded pinning-body-mutated \
  kprove "$CASE/pinning-body-mutated.k" \
  --definition "$BUILD/body-mutated-kompiled" \
  --spec-module PINNING-BODY-MUTATED

run_bounded body-mutated-false-program-proof \
  kprove "$CASE/body-mutation-spec.k" \
  --definition "$BUILD/body-mutated-kompiled" \
  --spec-module BODY-MUTATION-SPEC

run_bounded body-mutated-python-witness \
  python3 /audit-output/evidence/check_body_mutation.py

echo '$ SHA-256 of adequacy artifacts'
sha256sum \
  /audit-output/evidence/pinning-original.k \
  /audit-output/evidence/pinning-body-mutated.k \
  /audit-output/evidence/verification-body-mutated.k \
  /audit-output/evidence/body-mutation-spec.k \
  /audit-output/evidence/bridge-witnesses.k \
  /audit-output/evidence/ground-summary.k
echo "[exit $?]"
