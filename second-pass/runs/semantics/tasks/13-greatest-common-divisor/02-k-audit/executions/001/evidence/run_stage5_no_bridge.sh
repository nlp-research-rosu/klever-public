#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/source
EVIDENCE=/audit-output/evidence

printf 'COMMAND: cp %s %s\n' \
  "$EVIDENCE/verification-no-bridge.k" "$WORK/verification-no-bridge.k"
cp "$EVIDENCE/verification-no-bridge.k" "$WORK/verification-no-bridge.k"
copy_verification_status=$?
printf 'COPY VERIFICATION EXIT STATUS: %d\n' "$copy_verification_status"

printf 'COMMAND: cp %s %s\n' \
  "$EVIDENCE/spec-no-bridge.k" "$WORK/spec-no-bridge.k"
cp "$EVIDENCE/spec-no-bridge.k" "$WORK/spec-no-bridge.k"
copy_spec_status=$?
printf 'COPY SPEC EXIT STATUS: %d\n' "$copy_spec_status"

printf 'COMMAND: kompile %s --backend haskell --main-module GCD-VERIFICATION-NO-BRIDGE --syntax-module MPY-SYNTAX --output-definition %s --warnings none\n' \
  "$WORK/verification-no-bridge.k" "$WORK/verification-no-bridge-kompiled" \
  | tee "$EVIDENCE/stage5_no_bridge_compile.log"
kompile "$WORK/verification-no-bridge.k" \
  --backend haskell \
  --main-module GCD-VERIFICATION-NO-BRIDGE \
  --syntax-module MPY-SYNTAX \
  --output-definition "$WORK/verification-no-bridge-kompiled" \
  --warnings none \
  2>&1 | tee -a "$EVIDENCE/stage5_no_bridge_compile.log"
compile_status=${PIPESTATUS[0]}
printf 'EXIT STATUS: %d\n' "$compile_status" | tee -a "$EVIDENCE/stage5_no_bridge_compile.log"

printf 'COMMAND: kprove %s --definition %s --spec-module GCD-SPEC-NO-BRIDGE --claims program-correct-no-bridge --depth 80 --warnings none\n' \
  "$WORK/spec-no-bridge.k" "$WORK/verification-no-bridge-kompiled" \
  | tee "$EVIDENCE/stage5_no_bridge_proof.log"
kprove "$WORK/spec-no-bridge.k" \
  --definition "$WORK/verification-no-bridge-kompiled" \
  --spec-module GCD-SPEC-NO-BRIDGE \
  --claims program-correct-no-bridge \
  --depth 80 \
  --warnings none \
  2>&1 | tee -a "$EVIDENCE/stage5_no_bridge_proof.log"
proof_status=${PIPESTATUS[0]}
printf 'EXIT STATUS: %d\n' "$proof_status" | tee -a "$EVIDENCE/stage5_no_bridge_proof.log"

if (( copy_verification_status != 0 || copy_spec_status != 0 || compile_status != 0 )); then
  exit 1
fi

printf 'NO-BRIDGE DIAGNOSTIC PROOF EXIT STATUS: %d\n' "$proof_status"
exit 0
