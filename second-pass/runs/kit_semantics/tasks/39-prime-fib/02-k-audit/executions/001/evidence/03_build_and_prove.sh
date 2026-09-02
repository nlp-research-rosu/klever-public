#!/usr/bin/env bash
set -eu
set -o pipefail

scratch=/tmp/audit-work/39-prime-fib-audit
evidence=/audit-output/evidence

run_capture() {
  log=$1
  shift
  printf 'running %s\n' "$log"
  set +e
  (
    printf '$'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    rc=$?
    printf '[exit %d]\n' "$rc"
    exit "$rc"
  ) > "$evidence/$log" 2>&1
  rc=$?
  set -e
  return "$rc"
}

cd "$scratch"

echo "K toolchain"
run_capture 03_versions.log sh -c 'command -v kompile; command -v krun; command -v kprove; kompile --version; kprove --version'

echo "Concrete programs are exact solution.py plus a call"
head -n 19 /audit-output/evidence/03_concrete_n1.py | cmp -s - solution.py
head -n 19 /audit-output/evidence/03_concrete_n5.py | cmp -s - solution.py
head -n 19 /audit-output/evidence/03_concrete_n0.py | cmp -s - solution.py
cp /audit-output/evidence/03_concrete_n1.py .
cp /audit-output/evidence/03_concrete_n5.py .
cp /audit-output/evidence/03_concrete_n0.py .
python3 py2mpy.py 03_concrete_n1.py > 03_concrete_n1.mpy
python3 py2mpy.py 03_concrete_n5.py > 03_concrete_n5.mpy
python3 py2mpy.py 03_concrete_n0.py > 03_concrete_n0.mpy
cp 03_concrete_n1.mpy 03_concrete_n5.mpy 03_concrete_n0.mpy "$evidence/"

echo "Fresh LLVM definition from trusted copied semantics"
run_capture 03_kompile_llvm.log kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled

echo "Concrete boundary and normal executions"
run_capture 03_krun_n1.log krun 03_concrete_n1.mpy --definition runtime-audit-kompiled
run_capture 03_krun_n5.log krun 03_concrete_n5.mpy --definition runtime-audit-kompiled
run_capture 03_krun_n0.log krun 03_concrete_n0.mpy --definition runtime-audit-kompiled

echo "Fresh Haskell proof definition from copied source"
run_capture 03_kompile_haskell.log kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-audit-kompiled

echo "Positive target 1: inner loop"
run_capture 03_kprove_inner.log kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop

echo "Positive target 2: outer loop, using independently closed inner claim"
run_capture 03_kprove_outer.log kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop \
  --trusted SPEC.inner-loop

echo "Positive target 3: entry, using independently closed loop claims"
run_capture 03_kprove_entry.log kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop,SPEC.prime-fib \
  --trusted SPEC.inner-loop,SPEC.outer-loop

echo "all clean reconstruction commands exited 0"
