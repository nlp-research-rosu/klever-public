#!/usr/bin/env bash
set -u -o pipefail

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
cd "$scratch" || exit 1

run_logged() {
  local label=$1
  shift
  local output="$evidence/$label.log"
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" > "$output" 2>&1
  local status=$?
  cat "$output"
  printf 'EXIT_STATUS=%s\n' "$status"
  return "$status"
}

overall=0

printf '$ test ! -e runtime-kompiled -a ! -e verification-kompiled\n'
test ! -e runtime-kompiled -a ! -e verification-kompiled
status=$?
printf 'EXIT_STATUS=%s\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

printf '$ cp /audit-output/evidence/k_smoke.py /tmp/audit-work/reconstruction/k_smoke.py\n'
cp /audit-output/evidence/k_smoke.py "$scratch/k_smoke.py"
status=$?
printf 'EXIT_STATUS=%s\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

printf '$ python3 py2mpy.py k_smoke.py > k_smoke.mpy\n'
python3 py2mpy.py k_smoke.py > k_smoke.mpy
status=$?
printf 'EXIT_STATUS=%s\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

run_logged stage3-kompile-llvm \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-kompiled
status=$?
if [ "$status" -ne 0 ]; then overall=1; fi

run_logged stage3-krun-smoke \
  krun k_smoke.mpy --definition runtime-kompiled
status=$?
if [ "$status" -ne 0 ]; then overall=1; fi

run_logged stage3-kompile-haskell \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module VERIFICATION-SYNTAX \
    --output-definition verification-kompiled
status=$?
if [ "$status" -ne 0 ]; then overall=1; fi

run_logged stage3-kprove-pile-loop \
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.pile-loop
status=$?
if [ "$status" -ne 0 ]; then overall=1; fi

run_logged stage3-kprove-make-a-pile \
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.make-a-pile
status=$?
if [ "$status" -ne 0 ]; then overall=1; fi

run_logged stage3-kprove-all \
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module SPEC
status=$?
if [ "$status" -ne 0 ]; then overall=1; fi

printf 'CLEAN_RECONSTRUCTION_STATUS=%s\n' "$overall"
exit "$overall"
