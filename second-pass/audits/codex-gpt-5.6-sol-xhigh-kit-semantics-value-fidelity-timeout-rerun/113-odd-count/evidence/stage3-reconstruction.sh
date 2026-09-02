#!/usr/bin/env bash
set -u

SOURCE=/tmp/audit-work/source
BUILD=/tmp/audit-work/build
EVIDENCE=/audit-output/evidence
status=0

mkdir -p "$BUILD"

run_logged() {
  local label="$1"
  shift
  local log="$EVIDENCE/$label.log"
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@" > "$log" 2>&1
  local rc=$?
  printf '[exit %d]\n' "$rc" >> "$log"
  printf '[exit %d; log %s]\n' "$rc" "$log"
  tail -120 "$log"
  if (( rc != 0 )); then
    status=1
  fi
}

cd "$SOURCE" || exit 1

printf 'Stage 3: clean builds and positive target proofs\n'
printf 'K tool versions:\n'
kompile --version
kprove --version
krun --version

run_logged stage3-kompile-base-llvm \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition "$BUILD/base-llvm-kompiled"

printf '\n$ python3 /reference/py2mpy.py /audit-output/evidence/concrete_reconstruction_test.py > /tmp/audit-work/build/concrete_reconstruction_test.mpy\n'
python3 /reference/py2mpy.py "$EVIDENCE/concrete_reconstruction_test.py" \
  > "$BUILD/concrete_reconstruction_test.mpy"
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi

run_logged stage3-krun-base \
  krun "$BUILD/concrete_reconstruction_test.mpy" \
    --definition "$BUILD/base-llvm-kompiled"

run_logged stage3-kompile-verification-llvm \
  kompile verification.k \
    --backend llvm \
    --main-module VERIFICATION-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition "$BUILD/verification-llvm-kompiled"

run_logged stage3-krun-extended \
  krun "$BUILD/concrete_reconstruction_test.mpy" \
    --definition "$BUILD/verification-llvm-kompiled"

run_logged stage3-kompile-verification-haskell \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition "$BUILD/verification-kompiled"

run_logged stage3-kprove-odd-loop \
  kprove spec.k \
    --definition "$BUILD/verification-kompiled" \
    --spec-module SPEC \
    --claims SPEC.odd-loop

run_logged stage3-kprove-full \
  kprove spec.k \
    --definition "$BUILD/verification-kompiled" \
    --spec-module SPEC

printf '\nFresh compiled-definition roots:\n'
find "$BUILD" -maxdepth 1 -type d -name '*-kompiled' -printf '%f\n' | sort
printf '\nFinal stage3_status=%d\n' "$status"
exit "$status"
