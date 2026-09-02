#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/57-monotonic

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run command -v kompile
run command -v kprove
run command -v krun
run kompile --version
run kprove --version

run cp /audit-output/evidence/03_spec_claim_1.k "$WORK/spec-claim-1.k"
run cp /audit-output/evidence/03_spec_claim_2.k "$WORK/spec-claim-2.k"
run cp /audit-output/evidence/03_concrete_smoke.py "$WORK/concrete-smoke.py"

printf '\n$ python3 %q %q > %q\n' \
  "$WORK/py2mpy.py" "$WORK/concrete-smoke.py" "$WORK/concrete-smoke.mpy"
python3 "$WORK/py2mpy.py" "$WORK/concrete-smoke.py" > "$WORK/concrete-smoke.mpy"
status=$?
printf '[exit %d]\n' "$status"

run kompile "$WORK/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$WORK/runtime-kompiled"

run krun "$WORK/concrete-smoke.mpy" \
  --definition "$WORK/runtime-kompiled"

run kompile "$WORK/verification.k" \
  --backend haskell \
  --main-module MONOTONIC-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$WORK/verification-kompiled"

run kprove "$WORK/spec.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module MONOTONIC-SPEC

run kprove "$WORK/spec-claim-1.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module MONOTONIC-SPEC-CLAIM-1

run kprove "$WORK/spec-claim-2.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module MONOTONIC-SPEC-CLAIM-2
