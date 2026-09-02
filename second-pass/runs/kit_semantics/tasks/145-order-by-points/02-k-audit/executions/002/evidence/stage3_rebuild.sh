#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/145-order-by-points-002
evidence=/audit-output/evidence
overall=0

record_pipeline_status() {
  command_status=$1
  label=$2
  echo "EXIT ($label): $command_status"
  if [ "$command_status" -ne 0 ]; then
    overall=1
  fi
}

echo "$ cd $scratch"
cd "$scratch" || exit 1
echo "EXIT: 0"

echo "$ test ! -e audit-runtime-kompiled"
test ! -e audit-runtime-kompiled
record_pipeline_status "$?" "fresh runtime output path"
echo "$ test ! -e audit-verification-kompiled"
test ! -e audit-verification-kompiled
record_pipeline_status "$?" "fresh proof output path"

echo "$ python3 /reference/py2mpy.py /audit-output/evidence/concrete_probe.py > concrete_probe.mpy"
python3 /reference/py2mpy.py \
  /audit-output/evidence/concrete_probe.py \
  > concrete_probe.mpy
record_pipeline_status "$?" "translate concrete probe"

echo "$ kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled"
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled \
  2>&1 | tee "$evidence/stage3_llvm_compile.log"
record_pipeline_status "${PIPESTATUS[0]}" "fresh LLVM kompile"

echo "$ krun concrete_probe.mpy --definition audit-runtime-kompiled"
krun concrete_probe.mpy \
  --definition audit-runtime-kompiled \
  2>&1 | tee "$evidence/stage3_concrete_krun.log"
krun_status=${PIPESTATUS[0]}
record_pipeline_status "$krun_status" "fresh concrete krun"
if ! rg -U -q '<exc>[[:space:]]+NoExc[[:space:]]+</exc>' \
    "$evidence/stage3_concrete_krun.log"; then
  echo "MISSING expected NoExc final cell"
  overall=1
fi
if ! rg -U -q '<exit-code>[[:space:]]+0[[:space:]]+</exit-code>' \
    "$evidence/stage3_concrete_krun.log"; then
  echo "MISSING expected exit-code 0 final cell"
  overall=1
fi

echo "$ kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled"
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled \
  2>&1 | tee "$evidence/stage3_haskell_compile.log"
record_pipeline_status "${PIPESTATUS[0]}" "fresh Haskell kompile"

echo "$ kast solution.mpy --definition audit-verification-kompiled --module VERIFICATION-SYNTAX --sort Module --expand-macros --output kore > parsed-solution.kore"
kast solution.mpy \
  --definition audit-verification-kompiled \
  --module VERIFICATION-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  > parsed-solution.kore
record_pipeline_status "$?" "parse translated solution"

echo "$ kast --expression solutionModule --definition audit-verification-kompiled --module VERIFICATION-SYNTAX --sort Module --expand-macros --output kore > claim-solution.kore"
kast \
  --expression solutionModule \
  --definition audit-verification-kompiled \
  --module VERIFICATION-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  > claim-solution.kore
record_pipeline_status "$?" "expand claimed program"

echo "$ diff -u parsed-solution.kore claim-solution.kore"
diff -u parsed-solution.kore claim-solution.kore \
  | tee "$evidence/stage3_program_identity.diff"
record_pipeline_status "${PIPESTATUS[0]}" "constructor-level program identity"
sha256sum parsed-solution.kore claim-solution.kore \
  | tee "$evidence/stage3_program_identity.sha256"

for claim in digit-sum-loop digit-sum-function order-by-points; do
  proof_log="$evidence/stage3_kprove_${claim}.log"
  echo "$ kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.$claim"
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims "SPEC.$claim" \
    2>&1 | tee "$proof_log"
  proof_status=${PIPESTATUS[0]}
  record_pipeline_status "$proof_status" "kprove SPEC.$claim"
  if ! rg -q '^#Top$' "$proof_log"; then
    echo "MISSING #Top for SPEC.$claim"
    overall=1
  fi
done

echo "STAGE3 SCRIPT EXIT: $overall"
exit "$overall"
