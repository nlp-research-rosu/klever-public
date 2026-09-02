#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
summary="$evidence/03_reconstruction_summary.log"
: > "$summary"

run_to_log() {
  local label=$1
  shift
  local log="$evidence/03_${label}.log"
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } > "$log"
  "$@" >> "$log" 2>&1
  local status=$?
  printf '\n[exit %d]\n' "$status" >> "$log"
  printf '%s exit=%d log=%s\n' "$label" "$status" "$log" | tee -a "$summary"
  return "$status"
}

overall=0
cd "$work"

run_to_log translate_concrete \
  bash -c 'python3 /reference/py2mpy.py /audit-output/evidence/03_concrete_driver.py > /tmp/audit-work/reconstruction/03_concrete_driver.mpy' \
  || overall=1

run_to_log build_runtime \
  kompile --backend llvm reference-semantics/semantics.k \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-audit-kompiled \
  || overall=1

run_to_log concrete_run \
  krun 03_concrete_driver.mpy --definition runtime-audit-kompiled \
  || overall=1

run_to_log build_verification \
  kompile --backend haskell verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-audit-kompiled \
  || overall=1

run_to_log positive_all \
  kprove spec.k \
    --definition verification-audit-kompiled \
    --spec-module SPEC \
  || overall=1

for length in 0 1 2 3 4 5 6 7
do
  run_to_log "positive_len_${length}" \
    kprove spec.k \
      --definition verification-audit-kompiled \
      --spec-module SPEC \
      --claims "SPEC.len-${length}" \
    || overall=1
done

printf 'overall=%d\n' "$overall" | tee -a "$summary"
exit "$overall"
