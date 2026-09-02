#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruct-001
evidence=/audit-output/evidence
status_file=$evidence/stage3_status.log
: > "$status_file"
overall=0

run_logged() {
  name=$1
  shift
  log=$evidence/"$name".log
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } | tee -a "$status_file"
  "$@" > "$log" 2>&1
  rc=$?
  printf '%s exit=%d log=%s\n' "$name" "$rc" "$log" | tee -a "$status_file"
  if (( rc != 0 )); then
    overall=1
  fi
}

printf 'Scratch pre-build compiled-directory check\n' | tee -a "$status_file"
find "$scratch" -maxdepth 1 -type d -name '*-kompiled' -print \
  | tee -a "$status_file"

printf '$ cd %q && python3 py2mpy.py %q > %q\n' \
  "$scratch" \
  "$evidence/concrete_reconstruction.py" \
  "$scratch/concrete_reconstruction.mpy" \
  | tee -a "$status_file"
(
  cd "$scratch"
  python3 py2mpy.py \
    "$evidence/concrete_reconstruction.py" \
    > concrete_reconstruction.mpy
)
rc=$?
printf 'translate_concrete exit=%d\n' "$rc" | tee -a "$status_file"
if (( rc != 0 )); then
  overall=1
fi

cd "$scratch" || exit 2

run_logged \
  stage3_kompile_llvm \
  kompile --backend llvm reference-semantics/semantics.k \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-fresh-kompiled

run_logged \
  stage3_krun_concrete \
  krun concrete_reconstruction.mpy \
    --definition runtime-fresh-kompiled

run_logged \
  stage3_kompile_verification \
  kompile --backend haskell verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-fresh-kompiled

run_logged \
  stage3_kprove_loop \
  kprove spec.k \
    --definition verification-fresh-kompiled \
    --spec-module SPEC \
    --claims SPEC.loop-inv

run_logged \
  stage3_kprove_all \
  kprove spec.k \
    --definition verification-fresh-kompiled \
    --spec-module SPEC

run_logged \
  stage3_kompile_connection \
  kompile --backend haskell connection.k \
    --main-module CONNECTION \
    --syntax-module MPY-SYNTAX \
    --output-definition connection-fresh-kompiled

run_logged \
  stage3_kprove_connection \
  kprove connection-spec.k \
    --definition connection-fresh-kompiled \
    --spec-module CONNECTION-SPEC

printf 'overall=%d\n' "$overall" | tee -a "$status_file"
exit "$overall"
