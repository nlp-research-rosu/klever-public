#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/135-can-arrange
cd "$scratch" || exit 90

run_logged() {
  label=$1
  shift
  log="/audit-output/evidence/${label}.log"
  echo "COMMAND [$label]: $*"
  set +e
  "$@" 2>&1 | tee "$log"
  status=${PIPESTATUS[0]}
  set -e
  echo "EXIT [$label]: $status"
  return "$status"
}

overall=0

echo 'COMMAND: translate reviewer concrete smoke with trusted translator'
python3 trusted-py2mpy.py \
  /audit-output/evidence/reviewer_concrete_smoke.py \
  > reviewer-concrete-smoke.mpy
status=$?
echo "EXIT [translate-concrete-smoke]: $status"
if test "$status" -ne 0; then overall=1; fi

run_logged stage3_llvm_kompile \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-audit-kompiled
status=$?
if test "$status" -ne 0; then overall=1; fi

if test "$status" -eq 0; then
  run_logged stage3_krun_smoke \
    krun reviewer-concrete-smoke.mpy \
      --definition runtime-audit-kompiled
  status=$?
  if test "$status" -ne 0; then overall=1; fi
fi

run_logged stage3_connection_kompile \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION-BASE \
    --syntax-module MPY-SYNTAX \
    --output-definition connection-audit-kompiled
status=$?
if test "$status" -ne 0; then overall=1; fi

if test "$status" -eq 0; then
  for claim in \
    ge-int-int \
    ge-bool-bool \
    ge-bool-int \
    ge-int-bool \
    ge-float-float \
    ge-int-float \
    ge-float-int \
    ge-bool-float \
    ge-float-bool \
    ge-str-str
  do
    run_logged "stage3_connection_${claim}" \
      kprove connection-spec.k \
        --definition connection-audit-kompiled \
        --spec-module CONNECTION-SPEC \
        --claims "CONNECTION-SPEC.${claim}"
    status=$?
    if test "$status" -ne 0; then overall=1; fi
  done
fi

run_logged stage3_verification_kompile \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-audit-kompiled
status=$?
if test "$status" -ne 0; then overall=1; fi

if test "$status" -eq 0; then
  run_logged stage3_target_loop \
    kprove spec.k \
      --definition verification-audit-kompiled \
      --spec-module SPEC \
      --claims SPEC.can-arrange-loop
  status=$?
  if test "$status" -ne 0; then overall=1; fi

  run_logged stage3_target_all \
    kprove spec.k \
      --definition verification-audit-kompiled \
      --spec-module SPEC
  status=$?
  if test "$status" -ne 0; then overall=1; fi
fi

exit "$overall"
