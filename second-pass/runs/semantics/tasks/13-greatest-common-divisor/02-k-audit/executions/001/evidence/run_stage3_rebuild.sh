#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/source
EVIDENCE=/audit-output/evidence
overall=0

run_logged() {
  local label=$1
  shift
  local logfile="$EVIDENCE/stage3_${label}.log"
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } | tee "$logfile"
  "$@" 2>&1 | tee -a "$logfile"
  local status=${PIPESTATUS[0]}
  printf 'EXIT STATUS: %d\n' "$status" | tee -a "$logfile"
  if (( status != 0 )); then
    overall=1
  fi
}

run_logged versions kompile --version
run_logged compile_runtime \
  kompile "$WORK/reference-semantics/semantics.k" \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition "$WORK/runtime-kompiled" \
    --warnings none

printf 'COMMAND: python3 %s %s > %s\n' \
  "$WORK/py2mpy.py" \
  "$EVIDENCE/stage3_concrete_probe.py" \
  "$WORK/stage3_concrete_probe.mpy" \
  | tee "$EVIDENCE/stage3_translate_probe.log"
python3 "$WORK/py2mpy.py" "$EVIDENCE/stage3_concrete_probe.py" \
  > "$WORK/stage3_concrete_probe.mpy"
status=$?
printf 'EXIT STATUS: %d\n' "$status" | tee -a "$EVIDENCE/stage3_translate_probe.log"
if (( status != 0 )); then
  overall=1
fi

run_logged concrete_probe \
  krun "$WORK/stage3_concrete_probe.mpy" \
    --definition "$WORK/runtime-kompiled"

run_logged compile_verification \
  kompile "$WORK/verification.k" \
    --backend haskell \
    --main-module GCD-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition "$WORK/verification-kompiled" \
    --warnings none

for claim in euclid-step program-correct example-3-5 example-25-15; do
  label=${claim//-/_}
  run_logged "claim_${label}" \
    kprove "$WORK/spec.k" \
      --definition "$WORK/verification-kompiled" \
      --spec-module GCD-SPEC \
      --claims "$claim" \
      --warnings none
done

printf 'STAGE 3 OVERALL EXIT STATUS: %d\n' "$overall"
exit "$overall"
