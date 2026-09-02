#!/usr/bin/env bash
set -uo pipefail

CASE=/tmp/audit-work/case
BUILD=/tmp/audit-work/build
LOG=/audit-output/evidence/03-reconstruction.log
mkdir -p "$BUILD"
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
  if (( lines <= 100 )); then
    sed -n '1,100p' "$raw"
  else
    sed -n '1,60p' "$raw"
    echo "[... bounded omission: $((lines - 100)) lines ...]"
    tail -n 40 "$raw"
  fi
  echo "[end $label]"
  return 0
}

echo '$ kompile --version'
kompile --version
echo "[exit $?]"
echo '$ kprove --version'
kprove --version
echo "[exit $?]"

echo '$ python3 /audit-output/evidence/make_concrete_cases.py'
python3 /audit-output/evidence/make_concrete_cases.py
echo "[exit $?]"
echo '$ python3 /reference/py2mpy.py /tmp/audit-work/case/concrete-audit.py > /tmp/audit-work/case/concrete-audit.mpy'
python3 /reference/py2mpy.py "$CASE/concrete-audit.py" > "$CASE/concrete-audit.mpy"
echo "[exit $?]"

run_bounded llvm-kompile \
  kompile "$CASE/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$BUILD/runtime-kompiled"

run_bounded llvm-concrete \
  krun "$CASE/concrete-audit.mpy" \
  --definition "$BUILD/runtime-kompiled" \
  --output none

run_bounded base-kompile \
  kompile "$CASE/verification.k" \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition "$BUILD/base-kompiled"

run_bounded inner-proof \
  kprove "$CASE/spec.k" \
  --definition "$BUILD/base-kompiled" \
  --spec-module SPEC-INNER

run_bounded inner-kompile \
  kompile "$CASE/verification.k" \
  --backend haskell \
  --main-module VERIFICATION-WITH-INNER \
  --syntax-module MPY-SYNTAX \
  --output-definition "$BUILD/inner-kompiled"

run_bounded helper-proof \
  kprove "$CASE/spec.k" \
  --definition "$BUILD/inner-kompiled" \
  --spec-module SPEC-HELPER

run_bounded helper-kompile \
  kompile "$CASE/verification.k" \
  --backend haskell \
  --main-module VERIFICATION-WITH-HELPER \
  --syntax-module MPY-SYNTAX \
  --output-definition "$BUILD/helper-kompiled"

run_bounded outer-proof \
  kprove "$CASE/spec.k" \
  --definition "$BUILD/helper-kompiled" \
  --spec-module SPEC-OUTER

run_bounded outer-kompile \
  kompile "$CASE/verification.k" \
  --backend haskell \
  --main-module VERIFICATION-WITH-OUTER \
  --syntax-module MPY-SYNTAX \
  --output-definition "$BUILD/outer-kompiled"

run_bounded entry-proof \
  kprove "$CASE/spec.k" \
  --definition "$BUILD/outer-kompiled" \
  --spec-module SPEC-ENTRY

run_bounded entry-kompile \
  kompile "$CASE/verification.k" \
  --backend haskell \
  --main-module VERIFICATION-WITH-ENTRY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$BUILD/entry-kompiled"

run_bounded final-proof \
  kprove "$CASE/spec.k" \
  --definition "$BUILD/entry-kompiled" \
  --spec-module SPEC

echo '$ positive proof summary'
for label in inner-proof helper-proof outer-proof entry-proof final-proof; do
  status_text=$(grep -c '^#Top$' "$BUILD/${label}.raw.log")
  error_text=$(grep -c '\\[Error\\]' "$BUILD/${label}.raw.log")
  echo "$label top_lines=$status_text error_lines=$error_text"
done
